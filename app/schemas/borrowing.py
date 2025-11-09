from pydantic import BaseModel
from datetime import date
from .user import UserPublic
from .book import Book

class BorrowRecordBase(BaseModel):
    book_id: int

class BorrowRecordCreate(BorrowRecordBase):
    pass

class BorrowRecordPublic(BaseModel):
    id: int
    borrow_date: date
    return_date: date | None
    user: UserPublic
    book: Book
    
    class Config:
        from_attributes = True