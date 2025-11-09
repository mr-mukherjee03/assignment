from pydantic import BaseModel
from typing import List

class AuthorBase(BaseModel):
    name: str
    bio: str | None = None

class AuthorCreate(AuthorBase):
    pass

class AuthorPublic(AuthorBase):
    id: int
    class Config:
        from_attributes = True

class Author(AuthorBase):
    id: int
    
    books: List["BookPublic"] = []
    
    class Config:
        from_attributes = True