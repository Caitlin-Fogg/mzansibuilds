from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db
from app.routes.users import get_current_user

router = APIRouter(tags=["Collaboration Requests"])

# Helper function
def collab_to_response(req: models.CollaborationRequest, username: str, project_title: str):
    return schemas.CollaborationRequestResponse(
        id=req.id,
        project_id=req.project_id,
        project_title=project_title,
        user_id=req.user_id,
        username=username,
        message=req.message,
        status=req.status,
        created_at=req.created_at
    )

# Create collaboration request
@router.post("/projects/{project_id}/collaborate", response_model=schemas.CollaborationRequestResponse)
def request_collaboration(project_id: int, request: schemas.CollaborationRequestCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.user_id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot request collaboration on your own project")

    # Prevent duplicate requests
    existing = db.query(models.CollaborationRequest).filter(models.CollaborationRequest.project_id == project_id, models.CollaborationRequest.user_id == current_user.id).first()

    if existing:
        raise HTTPException(status_code=400, detail="Request already exists")

    db_request = models.CollaborationRequest(project_id=project_id, user_id=current_user.id, message=request.message)

    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return collab_to_response(db_request, current_user.username, project.title)


# View requests for a project (owner only)
@router.get("/projects/{project_id}/requests", response_model=List[schemas.CollaborationRequestResponse])
def get_requests(project_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    results = (
    db.query(models.CollaborationRequest, models.User.username, models.Project.title).join(models.User, models.CollaborationRequest.user_id == models.User.id).join(models.Project, models.CollaborationRequest.project_id == models.Project.id).filter(models.CollaborationRequest.project_id == project_id).all())

    return [collab_to_response(req, username, project_title) for req, username, project_title in results]

# Get user's requests
@router.get("/requests/me", response_model=List[schemas.CollaborationRequestResponse])
def get_my_requests(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    results = (
    db.query(models.CollaborationRequest, models.User.username, models.Project.title).join(models.User, models.CollaborationRequest.user_id == models.User.id).join(models.Project, models.CollaborationRequest.project_id == models.Project.id).filter(models.CollaborationRequest.user_id == current_user.id).order_by(models.CollaborationRequest.created_at.desc()).all())

    return [collab_to_response(req, username, project_title) for req, username, project_title in results]

# Accept request
@router.put("/requests/{request_id}/accept", response_model=schemas.CollaborationRequestResponse)
def accept_request(request_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    req = db.query(models.CollaborationRequest).filter(models.CollaborationRequest.id == request_id).first()

    if not req:
        raise HTTPException(status_code=404, detail="Request not found")

    project = db.query(models.Project).filter(models.Project.id == req.project_id).first()

    if project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    req.status = "accepted"

    db.commit()
    db.refresh(req)
    user = db.query(models.User).filter(models.User.id == req.user_id).first()
    return collab_to_response(req, user.username, project.title)


# Reject request
@router.put("/requests/{request_id}/reject", response_model=schemas.CollaborationRequestResponse)
def reject_request(request_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    req = db.query(models.CollaborationRequest).filter(models.CollaborationRequest.id == request_id).first()

    if not req:
        raise HTTPException(status_code=404, detail="Request not found")

    project = db.query(models.Project).filter(models.Project.id == req.project_id).first()

    if project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    req.status = "rejected"

    db.commit()
    db.refresh(req)
    user = db.query(models.User).filter(models.User.id == req.user_id).first()
    return collab_to_response(req, user.username, project.title)

# Delete request
@router.delete("/requests/{request_id}", status_code=204)
def delete_request(request_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    request = db.query(models.CollaborationRequest).filter(models.CollaborationRequest.id == request_id).first()

    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    if request.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(request)
    db.commit()
    return