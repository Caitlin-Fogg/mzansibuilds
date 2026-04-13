from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from typing import List
from app import models, schemas
from app.database import get_db
from app.routes.users import get_current_user

'''
Handles all project-related operations:
- Creating projects
- Retrieving projects (feeds)
- Updating and deleting projects
- Enforcing ownership-based access control
'''

router = APIRouter(prefix="/projects", tags=["Projects"])

# Helper function
# Convert SQLAlchemy project model to API response schema
# Adds related user information (username)
def project_to_response(p: models.Project) -> schemas.ProjectResponse:
    return schemas.ProjectResponse(
        id=p.id,
        title=p.title,
        description=p.description,
        stage=p.stage,
        support_needed=p.support_needed,
        status=p.status,
        user_id=p.user_id,
        username=p.owner.username,
        created_at=p.created_at
    )

# Create a project (requires login)
@router.post("/", response_model=schemas.ProjectResponse)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Assigns a project to the currently logged in user
    db_project = models.Project(**project.dict(), user_id=current_user.id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    db_project = db.query(models.Project).options(joinedload(models.Project.owner)).get(db_project.id)
    return project_to_response(db_project)

# List all projects
@router.get("/", response_model=List[schemas.ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    projects = db.query(models.Project).options(joinedload(models.Project.owner)).all()
    return [project_to_response(p) for p in projects]

# Get current user's projects
@router.get("/me", response_model=List[schemas.ProjectResponse])
def get_my_projects(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    projects = (db.query(models.Project).options(joinedload(models.Project.owner)).filter(models.Project.user_id == current_user.id).all())
    return [project_to_response(p) for p in projects]

# Live Feed Endpoint - get active projects
@router.get("/active", response_model=List[schemas.ProjectResponse])
def get_active_projects(db: Session = Depends(get_db),page: int = Query(1, ge=1),limit: int = Query(10, ge=1, le=100)):
    skip = (page - 1) * limit

    projects = (
        db.query(models.Project).options(joinedload(models.Project.owner)).filter(models.Project.status == "active").order_by(models.Project.created_at.desc()).offset(skip).limit(limit).all())

    return [project_to_response(p) for p in projects]

# Celebration Wall Endpoint - get completed projects
@router.get("/completed", response_model=List[schemas.ProjectResponse])
def get_completed_projects(db: Session = Depends(get_db), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    skip = (page - 1) * limit

    projects = (db.query(models.Project).options(joinedload(models.Project.owner)).filter(models.Project.status == "completed").order_by(models.Project.created_at.desc()).offset(skip).limit(limit).all())

    return [project_to_response(p) for p in projects]


# Get a single project
@router.get("/{project_id}", response_model=schemas.ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).options(joinedload(models.Project.owner)).filter(models.Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project_to_response(project)

# Update a project (only owner can update)
@router.put("/{project_id}", response_model=schemas.ProjectResponse)
def update_project(project_id: int, updated_project: schemas.ProjectUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this project")

    # Only update provided fields
    for key, value in updated_project.dict(exclude_unset=True).items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)
    project = db.query(models.Project).options(joinedload(models.Project.owner)).get(project.id)
    return project_to_response(project)

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

