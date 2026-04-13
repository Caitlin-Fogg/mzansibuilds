from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

'''
This file defines SQLAlchemy models that map to database tables
These models represent the structure of the database and relationships between entities
'''

# User Model - stores registered user information
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    projects = relationship("Project", back_populates="owner", cascade="all, delete, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete, delete-orphan")
    collaboration_requests = relationship("CollaborationRequest", back_populates="user", cascade="all, delete, delete-orphan")


# Project Model - each project belongs to a user (owner)
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    stage = Column(String)
    support_needed = Column(String)
    status = Column(String, default="active")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("status IN ('active','completed')", name="projects_status_chk"),
    )

    # Relationships
    owner = relationship("User", back_populates="projects")
    milestones = relationship("Milestone", back_populates="project", cascade="all, delete, delete-orphan")
    comments = relationship("Comment", back_populates="project", cascade="all, delete, delete-orphan")
    collaboration_requests = relationship("CollaborationRequest", back_populates="project", cascade="all, delete, delete-orphan")


# Milestone Model - represents a project milestone linked to a specific project
class Milestone(Base):
    __tablename__ = "milestones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    title = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    project = relationship("Project", back_populates="milestones")


# Comment Model - stores comments made by users on projects
class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="comments")
    user = relationship("User", back_populates="comments")


# CollaborationRequest Model - tracks requests made by users to collaborate on projects
class CollaborationRequest(Base):
    __tablename__ = "collaboration_requests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    message = Column(Text)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("status IN ('pending','accepted','rejected')", name="collab_status_chk"),
    )

    # Relationships
    project = relationship("Project", back_populates="collaboration_requests")
    user = relationship("User", back_populates="collaboration_requests")