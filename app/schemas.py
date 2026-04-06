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

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)

class UserDelete(BaseModel):
    password: str

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

# Milestone Schemas
class MilestoneBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class MilestoneCreate(MilestoneBase):
    pass


class MilestoneResponse(MilestoneBase):
    id: int
    project_id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Comment Schemas
class CommentBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)


class CommentCreate(CommentBase):
    pass


class CommentResponse(CommentBase):
    id: int
    project_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True