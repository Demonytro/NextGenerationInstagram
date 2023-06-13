import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.database.db import get_db

from src.routes import images, comments


app = FastAPI()

templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory="static"), name='static')


@app.get('/', response_class=HTMLResponse)
# <<<<<<< Daniil
# def home(request: Request):
# =======
async def home(request: Request):
# >>>>>>> dev
    return templates.TemplateResponse('index.html', {"request": request})


@app.get("/api/healthchecker")
# <<<<<<< Daniil
def healthchecker(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail="Error connecting to the database")


app.include_router(images.router, prefix="/api")
app.include_router(comments.router, prefix='/api')

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
# =======
# async def healthchecker(db: Session = Depends(get_db)):
#     try:
#         result = db.execute(text("SELECT 1")).fetchone()
#         if result is None:
#             raise HTTPException(status_code=500, detail="Database is not configured correctly")
#         return {"message": "Welcome to FastAPI!"}
#     except Exception as e:
#         print(e)
#         raise HTTPException(status_code=500, detail="Error connecting to the database")


# app.include_router(images.router, prefix="/api")


# if __name__ == '__main__':
#     uvicorn.run("main:app", host='localhost', port=8000, reload=True)
# >>>>>>> dev
