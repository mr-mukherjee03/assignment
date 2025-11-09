# Development Notes

[cite_start]This document details the development process, challenges faced, and solutions implemented for the Book Library Management API assignment[cite: 57].

### [cite_start]What challenges did you face while building this? [cite: 58]

1.  **Circular Pydantic Models:** The most significant challenge was the circular dependency between `Author` and `Book` schemas. [cite_start]The `Author` schema needed to include a list of `Book` schemas, and the `Book` schema needed to include its `Author`[cite: 31, 39]. A direct import created a `NameError` or `ImportError`.

2.  [cite_start]**Transactional Logic for Borrowing:** The `POST /api/v1/borrow` endpoint [cite: 41] required two separate database operations that had to succeed or fail together:
    1.  Creating a new `BorrowRecord` in its table.
    2.  Updating the `is_available` status of the `Book` in its table.
    If the `BorrowRecord` was created but updating the `Book` failed (or vice-versa), the database would be in an inconsistent state.

3.  [cite_start]**Implementing Search and Filtering:** The `GET /api/v1/books` endpoint needed to support optional search (by title) and filtering (by availability)[cite: 35]. Building this as a single, efficient SQLAlchemy query required dynamically adding `filter` conditions without hardcoding them.

### [cite_start]How did you solve them? [cite: 59]

1.  **Circular Models:** I solved this by using Pydantic's `model_rebuild()` method (or `update_forward_refs()` in Pydantic v1). I defined a simple `BookBase` schema in `author.py` for the list in the `Author` model. Then, in the `book.py` schema, I imported the `AuthorPublic` schema. Finally, at the end of `author.py`, I called `Book.model_rebuild()` to allow Pydantic to resolve the forward references correctly after all models were defined.

2.  **Transactional Logic:** I used the SQLAlchemy `Session` object (`db`) as a single unit of work. In the `borrow_book` endpoint, I added the `new_record` and updated the `book.is_available` property. I then called `db.commit()` *only once* at the very end. This ensures that both changes are sent to the database as a single transaction. If any part fails, the `db.close()` in the `finally` block of the `get_db` dependency will roll back the transaction, preventing inconsistent data.

3.  **Search and Filtering:** I started with a base query (`query = db.query(models.Book)`). Then, I used `if` statements to check if the optional `search` or `available` query parameters were provided. If they were, I dynamically added `.filter()` conditions to the `query` object *before* finally calling `.all()` (or `.offset().limit().all()`). This builds a clean, single query instead of fetching all data and filtering in Python.

### [cite_start]What would you do differently if you had more time? [cite: 60]

* **User Roles (Admin vs. User):** I would add roles to the `User` model. This would allow me to restrict destructive endpoints (like `DELETE /books/` or `POST /authors/`) to "Admin" users only, while "User" accounts could only browse and borrow.
* **Refresh Tokens:** Currently, the JWT token expires in 30 minutes, and the user must log in again. I would implement a more robust system with short-lived access tokens and long-lived refresh tokens stored securely (perhaps in an `httpOnly` cookie) to provide a seamless user experience.
* **Async Database Calls:** I used synchronous database calls (`db.query(...)`) for simplicity and speed. With more time, I would integrate an async database driver (like `asyncpg` for PostgreSQL) and make all database interactions asynchronous using `async/await` to improve performance under load.
* [cite_start]**More Advanced Validation:** I would add business-level validation, such as preventing a user from borrowing more than 5 books at a time or preventing a book from beind deleted if it's currently on loan[cite: 38]. (Note: I did add the check for deleting borrowed books).

### [cite_start]What did you learn from this assignment? [cite: 61]

This assignment was an excellent exercise in building a complete, production-style API.
* I learned the practical importance of **FastAPI's Dependency Injection** system, not just for `get_db` but for creating a reusable, robust `get_current_user` dependency that secures endpoints.
* I gained a much deeper understanding of the **relationship between SQLAlchemy ORM models and Pydantic schemas**. They look similar but serve different purposes (database tables vs. API data shapes), and linking them with `Config: from_attributes = True` is powerful.
* I solidified my understanding of **transactional integrity** and how the `db.commit()` call is the single point of truth for a set of related database changes.
* [cite_start]I learned how to **structure a project in a modular way** [cite: 51][cite_start], separating routers, schemas, and database logic, which makes the code far more readable and maintainable[cite: 71].