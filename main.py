import uvicorn
from fastapi import FastAPI
from routes import cloudinary
from configure.config import settings


app = FastAPI()

@app.get("/")
def root():
    """
    The root function is a simple endpoint that returns a welcome message.

    :return: A dictionary with a message
    """
    return {"message": "Welcome to API!"}


app.include_router(cloudinary.router, prefix='/api')
