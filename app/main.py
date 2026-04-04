from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "MzansiBuilds API is running"}