from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from datetime import datetime

# Allowed values
ProjectStage = Literal["idea", "planning", "development", "completed"]
ProjectStatus = Literal["active", "completed"]

# User Schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=50)

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True  # Required for SQLAlchemy model compatibility


# Project Schemas
class ProjectBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    stage: Optional[ProjectStage] = None
    support_needed: Optional[str] = Field(None, max_length=500)
    status: Optional[ProjectStatus] = "active"

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime
    user_id: int

    class Config:
        orm_mode = True