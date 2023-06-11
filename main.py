import uvicorn
from fastapi import FastAPI
from routes import cloudinary
from configure.config import settings


app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to API!"}


app.include_router(cloudinary.router, prefix='/api')
