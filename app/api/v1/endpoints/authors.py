from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload
from typing import List

from app.db import models
from app.db.session import get_db
from app.schemas import author as author_schema
from app.api.v1.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=author_schema.Author)
def create_author(
    author: author_schema.AuthorCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) # This protects the endpoint
):
    new_author = models.Author(**author.model_dump())
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author

@router.get("/", response_model=List[author_schema.Author])
def get_authors(
    skip: int = 0, limit: int = 10, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    authors = db.query(models.Author).offset(skip).limit(limit).all()
    return authors

@router.get("/{author_id}", response_model=author_schema.Author)
def get_author(
    author_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Use selectinload to eager-load books as required 
    author = db.query(models.Author).options(
        selectinload(models.Author.books)
    ).filter(models.Author.id == author_id).first()
    
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author