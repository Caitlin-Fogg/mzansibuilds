from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db
from app.routes.users import get_current_user

'''
Handles project comments:
- Creating comments
- Retrieving comments for a project
- Deleting comments (with ownership enforcement)
'''

router = APIRouter(tags=["Comments"])

# Helper function
# Convert Comment model to response schema including username
def comment_to_response(comment: models.Comment, username: str) -> schemas.CommentResponse:
    return schemas.CommentResponse(
        id=comment.id,
        content=comment.content,
        user_id=comment.user_id,
        username=username,
        project_id=comment.project_id,
        created_at=comment.created_at
    )


# Create comment
@router.post("/projects/{project_id}/comments", response_model=schemas.CommentResponse)
def create_comment(project_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user),):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Create new comment
    db_comment = models.Comment(content=comment.content, project_id=project_id, user_id=current_user.id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)

    # Return response including username
    return comment_to_response(db_comment, current_user.username)

# Get comments for a project
@router.get("/projects/{project_id}/comments", response_model=List[schemas.CommentResponse])
def get_comments(project_id: int, db: Session = Depends(get_db)):

    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Join with User table to fetch usernames efficiently
    results = (db.query(models.Comment, models.User.username).join(models.User, models.Comment.user_id == models.User.id).filter(models.Comment.project_id == project_id).all())

    return [comment_to_response(comment, username) for comment, username in results]

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