from fastapi import FastAPI
from app.api.v1.api import api_router
from app.db.base import Base
from app.db.session import engine


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Book Library Management API",
    description="A backend system to manage a digital library."
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Book Library API"}