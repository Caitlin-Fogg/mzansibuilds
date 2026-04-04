from fastapi import FastAPI
from app.database import engine, Base
import app.models

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "MzansiBuilds API is running"}