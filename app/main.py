from fastapi import FastAPI
from app.database import engine
from app.models import user
from .routes import auth

app = FastAPI()

user.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
@app.get("/")
def root():
    return {"message": "Loopin backend is running"}