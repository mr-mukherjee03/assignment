from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import models
from app.db.session import get_db
from app.schemas import book as book_schema
from app.api.v1.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=book_schema.Book, status_code=status.HTTP_201_CREATED)
def create_book(
    book: book_schema.BookCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # --- TODO: Check if author_id exists ---
    # RESOLVED:
    author = db.query(models.Author).filter(models.Author.id == book.author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    new_book = models.Book(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.get("/", response_model=List[book_schema.Book])
def get_books(
    search: str | None = None, # For search
    available: bool | None = None, # For filter
    skip: int = 0, limit: int = 10,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # --- TODO: Add search and filter logic to the query ---
    # RESOLVED:
    # Start with a base query
    query = db.query(models.Book)
    
    # Apply filter for search (case-insensitive)
    if search:
        query = query.filter(models.Book.title.ilike(f"%{search}%"))
        
    # Apply filter for availability
    if available is not None:
        query = query.filter(models.Book.is_available == available)
        
    # Apply pagination
    books = query.offset(skip).limit(limit).all()
    return books

@router.get("/{book_id}", response_model=book_schema.Book)
def get_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.patch("/{book_id}", response_model=book_schema.Book)
def update_book(
    book_id: int,
    book_in: book_schema.BookUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Check if a new author_id is being provided and if it exists
    if book_in.author_id:
        author = db.query(models.Author).filter(models.Author.id == book_in.author_id).first()
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")

    # Get the update data, excluding unset values
    update_data = book_in.model_dump(exclude_unset=True)
    
    # Update the book object
    for key, value in update_data.items():
        setattr(book, key, value)
        
    db.commit()
    db.refresh(book)
    return book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if not book.is_available:
         raise HTTPException(status_code=400, detail="Cannot delete a book that is currently borrowed")

    db.delete(book)
    db.commit()
    return