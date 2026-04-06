from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db
from app.routes.users import get_current_user

router = APIRouter(tags=["Comments"])


# Create comment
@router.post("/projects/{project_id}/comments", response_model=schemas.CommentResponse)
def create_comment(project_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db_comment = models.Comment(content=comment.content, project_id=project_id, user_id=current_user.id)

    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


# Get comments for a project
@router.get("/projects/{project_id}/comments", response_model=List[schemas.CommentResponse])
def get_comments(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return db.query(models.Comment).filter(models.Comment.project_id == project_id).all()


# Update comment (only owner)
@router.put("/comments/{comment_id}", response_model=schemas.CommentResponse)
def update_comment(comment_id: int, updated: schemas.CommentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    comment.content = updated.content

    db.commit()
    db.refresh(comment)
    return comment


# Delete comment (only owner)
@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(comment)
    db.commit()
    return