from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db
from app.routes.users import get_current_user

router = APIRouter(prefix="/projects", tags=["Projects"])


# Create a project (requires login)
@router.post("/", response_model=schemas.ProjectResponse)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    project.user_id = current_user.id
    db_project = models.Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


# List all projects
@router.get("/", response_model=List[schemas.ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    projects = db.query(models.Project).all()
    return projects