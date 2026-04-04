from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str  # For creating a new user

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True  # Required for SQLAlchemy model compatibility


# Project Schemas
class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    stage: Optional[str] = None
    support_needed: Optional[str] = None
    status: Optional[str] = "active"

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime
    user_id: int

    class Config:
        orm_mode = True