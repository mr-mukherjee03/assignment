from pydantic import BaseModel
from datetime import date
from typing import List

from .author import AuthorPublic, Author

class BookBase(BaseModel):
    title: str
    publication_date: date | None = None
    author_id: int

class BookCreate(BookBase):
    pass
    
class BookUpdate(BaseModel):
    title: str | None = None
    publication_date: date | None = None
    is_available: bool | None = None
    author_id: int | None = None


class BookPublic(BaseModel):
    id: int
    title: str
    class Config:
        from_attributes = True

class Book(BookBase):
    id: int
    is_available: bool
    author: AuthorPublic
    class Config:
        from_attributes = True


Author.model_rebuild()