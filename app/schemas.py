from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal, List
from datetime import datetime

# Allowed values
ProjectStage = Literal["idea", "planning", "development", "completed"]
ProjectStatus = Literal["active", "completed"]
CollabStatus = Literal["pending", "accepted", "rejected"]

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
        from_attributes = True  # Required for SQLAlchemy model compatibility


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

class MilestoneListResponse(BaseModel):
    project_owner_id: int
    milestones: list[MilestoneResponse]

    class Config:
        from_attributes = True
    

# Comment Schemas
class CommentBase(BaseModel):
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