from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.db import models
from app.db.session import get_db
from app.schemas import borrowing as borrowing_schema
from app.api.v1.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=borrowing_schema.BorrowRecordPublic, status_code=status.HTTP_201_CREATED)
def borrow_book(
    borrow_request: borrowing_schema.BorrowRecordCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    
    book = db.query(models.Book).filter(models.Book.id == borrow_request.book_id).first()
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
        
   
    if not book.is_available:
        raise HTTPException(status_code=400, detail="Book is not available")
    
    new_record = models.BorrowRecord(
        user_id=current_user.id,
        book_id=book.id,
        borrow_date=date.today()
    )
    book.is_available = False
    
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

@router.post("/return/{record_id}", response_model=borrowing_schema.BorrowRecordPublic)
def return_book(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    record = db.query(models.BorrowRecord).filter(
        models.BorrowRecord.id == record_id,
        models.BorrowRecord.user_id == current_user.id
    ).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    if record.return_date:
        raise HTTPException(status_code=400, detail="Book already returned")
        
    book = db.query(models.Book).filter(models.Book.id == record.book_id).first()
    if book:
        book.is_available = True
        
    record.return_date = date.today()
    
    db.commit()
    db.refresh(record)
    return record

@router.get("/history", response_model=List[borrowing_schema.BorrowRecordPublic])
def get_borrowing_history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    history = db.query(models.BorrowRecord).filter(
        models.BorrowRecord.user_id == current_user.id
    ).all()
    return history