from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
import app.models
from app.routes import users, projects, milestones, comments, collaborations
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app.mount("/frontend", StaticFiles(directory=os.path.join(BASE_DIR, "frontend")), name="frontend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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