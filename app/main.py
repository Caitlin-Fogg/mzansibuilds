from fastapi import FastAPI
from app.database import engine, Base
import app.models
from app.routes import users, projects, milestones, comments, collaborations

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(projects.router)
app.include_router(milestones.router)
app.include_router(comments.router)
app.include_router(collaborations.router)

@app.get("/")
def root():
    return {"message": "MzansiBuilds API is running"}