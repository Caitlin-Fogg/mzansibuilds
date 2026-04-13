from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal, List
from datetime import datetime

'''
This file defines Pydantic schemas used for:
- Validating incoming request data
- Structuring API responses
- Ensuring data consistency between client and server
'''

# Allowed values - restricts values for certain fields to help with input validation
ProjectStage = Literal["idea", "planning", "development", "completed"]
ProjectStatus = Literal["active", "completed"]
CollabStatus = Literal["pending", "accepted", "rejected"]

# User Schemas
# Base schema shared across user-related operations
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr

# Schema used when registering a new user (includes password)
class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=50)

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)

class UserDelete(BaseModel):
    password: str

 # Schema returned to the client (excludes sensitive data like password)
class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Required for SQLAlchemy model compatibility


# Project Schemas
# Base project schema with validation rules to ensure clean and safe input
class ProjectBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    stage: Optional[ProjectStage] = None
    support_needed: Optional[str] = Field(None, max_length=500)
    status: Optional[ProjectStatus] = "active"

class ProjectCreate(ProjectBase):
    pass

# All fields optional to allow partial updates
class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    stage: Optional[ProjectStage] = None
    support_needed: Optional[str] = None
    status: Optional[ProjectStatus] = None

# Response schema includes additional fields such as user info and timestamps
class ProjectResponse(ProjectBase):
    id: int
    title: str
    description: str | None = None
    stage: str
    support_needed: str
    status: str
    user_id: int
    username: str 
    created_at: datetime

    class Config:
        from_attributes = True

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
        from_attributes = True

# Wrapper response including project owner and associated milestones
class MilestoneListResponse(BaseModel):
    project_owner_id: int
    milestones: list[MilestoneResponse]

    class Config:
        from_attributes = True
    

# Comment Schemas
class CommentBase(BaseModel):
    # Ensures comments are not empty and limits size
    content: str = Field(..., min_length=1, max_length=1000)


class CommentCreate(CommentBase):
    pass


class CommentResponse(CommentBase):
    id: int
    project_id: int
    user_id: int
    username: str 
    created_at: datetime

    class Config:
        from_attributes = True

# Collaboration Request Schemas
class CollaborationRequestBase(BaseModel):
    message: Optional[str] = Field(None, max_length=500)


class CollaborationRequestCreate(CollaborationRequestBase):
    pass


class CollaborationRequestResponse(CollaborationRequestBase):
    id: int
    project_id: int
    project_title: str
    user_id: int
    username: str
    status: CollabStatus
    created_at: datetime

    class Config:
        from_attributes = True