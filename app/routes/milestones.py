from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db
from app.routes.users import get_current_user

'''
Handles project milestones:
- Creating milestones for a project
- Retrieving milestones
- Deleting milestones
Includes ownership checks to ensure only project owners can modify milestones
'''

router = APIRouter(tags=["Milestones"])

# Helper function
# Convert Milestone model to API response format
def milestone_to_response(milestone: models.Milestone) -> schemas.MilestoneResponse:
    return schemas.MilestoneResponse(
        id=milestone.id,
        title=milestone.title,
        description=milestone.description,
        project_id=milestone.project_id,
        created_at=milestone.created_at
    )

# Create milestone
@router.post("/projects/{project_id}/milestones", response_model=schemas.MilestoneResponse)
def create_milestone(project_id: int, milestone: schemas.MilestoneCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db_milestone = models.Milestone(**milestone.dict(), project_id=project_id)

    db.add(db_milestone)
    db.commit()
    db.refresh(db_milestone)
    return milestone_to_response(db_milestone)


# Get milestones for a project (publicly available)
@router.get("/projects/{project_id}/milestones", response_model=schemas.MilestoneListResponse)
def get_milestones(project_id: int, db: Session = Depends(get_db)):

    project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    milestones = db.query(models.Milestone).filter(models.Milestone.project_id == project_id).order_by(models.Milestone.created_at.desc()).all()

    return {"project_owner_id": project.user_id, "milestones": [milestone_to_response(m) for m in milestones]}


# Delete milestone
@router.delete("/milestones/{milestone_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_milestone(milestone_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    milestone = db.query(models.Milestone).filter(models.Milestone.id == milestone_id).first()

    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")

    project = db.query(models.Project).filter(models.Project.id == milestone.project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(milestone)
    db.commit()
    return