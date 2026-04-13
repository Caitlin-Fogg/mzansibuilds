from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app import models, schemas
from app.database import SessionLocal, engine
from app.database import get_db
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt

'''
Handles all user-related functionality including:
- Registration
- Authentication (login with JWT)
- Profile management
- Secure password handling
'''

# Router setup
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Security settings
# Secret key used to sign JWT tokens (must be kept secure in production)
SECRET_KEY = "your-very-secret-key"
# Algorithm used for token signing
ALGORITHM = "HS256"
# Token expiry duration
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Password hashing context using Argon2 (secure hashing algorithm)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
# OAuth2 scheme used to extract token from requests
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

# Helper functions
# Hash plain text password before storing in database
def hash_password(password: str):
    return pwd_context.hash(password)

# Verify plain password against hashed password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Generate JWT access token with expiration time
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Extract and validate user from JWT token
# Used to protect routes that require authentication
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Decodes JWT token and extracts user details
    # If token is invalid or expired it raises authentication error
    # Retrieves user from database using email stored in token
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("user_id") 
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# Create a new user
@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if username or email already exists to prevent duplicates
    existing_user = db.query(models.User).filter((models.User.username == user.username) | (models.User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    # Create new user
    new_user = models.User(username=user.username, email=user.email, password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Login user - verifies email and password, returns the token for authenticated access
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    token = create_access_token(data={"sub": user.email, "user_id": user.id}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": token, "token_type": "bearer"}

# Get current logged in user profile
@router.get("/me", response_model=schemas.UserResponse)
def read_current_user(current_user: models.User = Depends(get_current_user)):
    return current_user

# Get a user by ID
@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update user - only accessible to authenticated user
@router.put("/me", response_model=schemas.UserResponse)
def update_user(updated_user: schemas.UserUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Check if new username/email already exists
    if updated_user.username:
        existing = db.query(models.User).filter(models.User.username == updated_user.username, models.User.id != current_user.id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Username already taken")

    if updated_user.email:
        existing = db.query(models.User).filter(models.User.email == updated_user.email, models.User.id != current_user.id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already taken")

    # Update fields
    if updated_user.username:
        current_user.username = updated_user.username

    if updated_user.email:
        current_user.email = updated_user.email

    if updated_user.password:
        current_user.password = hash_password(updated_user.password)

    db.commit()
    db.refresh(current_user)

    return current_user

# Delete user - requires password confirmation
@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_data: schemas.UserDelete, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Verify password
    if not verify_password(user_data.password, current_user.password):
        raise HTTPException(status_code=401, detail="Incorrect password"
        )

    db.delete(current_user)
    db.commit()
    return