from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from typing import List
from app import models, schemas
from app.database import get_db
from app.routes.users import get_current_user

router = APIRouter(prefix="/projects", tags=["Projects"])


# Create a project (requires login)
@router.post("/", response_model=schemas.ProjectResponse)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_project = models.Project(**project.dict(), user_id=current_user.id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    return schemas.ProjectResponse(id=db_project.id, title=db_project.title, description=db_project.description, stage=db_project.stage, support_needed=db_project.support_needed, status=db_project.status, user_id=db_project.user_id, username=current_user.username, created_at=db_project.created_at)


# List all projects
@router.get("/", response_model=List[schemas.ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    projects = db.query(models.Project).options(joinedload(models.Project.owner)).all()
    return [
        schemas.ProjectResponse(id=p.id, title=p.title, description=p.description, stage=p.stage, support_needed=p.support_needed, status=p.status, user_id=p.user_id, username=p.owner.username, created_at=p.created_at)
        for p in projects
    ]

# Get current user's projects
@router.get("/me", response_model=List[schemas.ProjectResponse])
def get_my_projects(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    projects = db.query(models.Project).options(joinedload(models.Project.owner)).filter(models.Project.user_id == current_user.id).all()
    return [
        schemas.ProjectResponse(id=p.id, title=p.title, description=p.description, stage=p.stage, support_needed=p.support_needed, status=p.status, user_id=p.user_id, username=p.owner.username, created_at=p.created_at)
        for p in projects
    ]
# Live Feed Endpoint
@router.get("/active", response_model=List[schemas.ProjectResponse])
def get_active_projects(db: Session = Depends(get_db),page: int = Query(1, ge=1),limit: int = Query(10, ge=1, le=100)):
    skip = (page - 1) * limit

    projects = (db.query(models.Project).options(joinedload(models.Project.owner)).filter(models.Project.status == "active").order_by(models.Project.created_at.desc()).offset(skip).limit(limit).all())

    # Include username in schema
    return [
        schemas.ProjectResponse(id=p.id, title=p.title, description=p.description, stage=p.stage, support_needed=p.support_needed, status=p.status, user_id=p.user_id, username=p.owner.username, created_at=p.created_at)
        for p in projects
    ]

# Celebration Wall Endpoint
@router.get("/completed", response_model=List[schemas.ProjectResponse])
def get_completed_projects(db: Session = Depends(get_db), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    skip = (page - 1) * limit

    projects = (db.query(models.Project).options(joinedload(models.Project.owner)).filter(models.Project.status == "completed").order_by(models.Project.created_at.desc()).offset(skip).limit(limit).all())

    return [
        schemas.ProjectResponse(id=p.id, title=p.title, description=p.description, stage=p.stage, support_needed=p.support_needed, status=p.status, user_id=p.user_id, username=p.owner.username, created_at=p.created_at)
        for p in projects
    ]



# Get a single project
@router.get("/{project_id}", response_model=schemas.ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).options(joinedload(models.Project.owner)).filter(models.Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Build response manually to include username
    return schemas.ProjectResponse(id=project.id, title=project.title, description=project.description, stage=project.stage, support_needed=project.support_needed, status=project.status, user_id=project.user_id, username=project.owner.username, created_at=project.created_at)


# Update a project (only owner can update)
@router.put("/{project_id}", response_model=schemas.ProjectResponse)
def update_project(
    project_id: int, updated_project: schemas.ProjectCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this project"
        )

    for key, value in updated_project.dict().items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)
    return schemas.ProjectResponse(id=project.id, title=project.title, description=project.description, stage=project.stage, support_needed=project.support_needed, status=project.status, user_id=project.user_id, username=project.owner.username, created_at=project.created_at)


# Delete a project (only owner can delete)
@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this project")

    db.delete(project)
    db.commit()
    return

