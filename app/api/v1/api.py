from fastapi import APIRouter
from app.api.v1.endpoints import auth, authors, books, borrowing

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(authors.router, prefix="/authors", tags=["Authors"])
api_router.include_router(books.router, prefix="/books", tags=["Books"])
api_router.include_router(borrowing.router, prefix="/borrow", tags=["Borrowing"])