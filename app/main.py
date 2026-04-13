# FastAPI core framework and middleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Used to serve static frontend files (HTML, CSS, JS)
from fastapi.staticfiles import StaticFiles
# Database engine and base model for table creation
from app.database import engine, Base
# Import models so SQLAlchemy can detect them when creating tables
import app.models
# Import route modules for different features of the application
from app.routes import users, projects, milestones, comments, collaborations
# OS module used for resolving file paths
import os

'''
Entry point of the FastAPI application, used for:
- Initialising the app
- Configuring middleware (CORS)
- Serving static frontend files
- Registering API routes
- Creating database tables
'''

# Create FastAPI application instance
app = FastAPI()

# Determine base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Mount the frontend folder so it can be accessed via /frontend URL
# This allows serving static files like HTML, CSS, and JavaScript
app.mount("/frontend", StaticFiles(directory=os.path.join(BASE_DIR, "frontend")), name="frontend")

# Configure CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
# This runs at startup and ensures all tables exist
Base.metadata.create_all(bind=engine)

# Register API routes from different modules
# Each router handles a specific feature of the application
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(milestones.router)
app.include_router(comments.router)
app.include_router(collaborations.router)

# Root endpoint to verify that the API is running
@app.get("/")
def root():
    return {"message": "MzansiBuilds API is running"}