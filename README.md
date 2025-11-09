# Book Library Management API (FastAPI)

This project is a REST API for a Book Library Management System, built as a technical assignment for CreativeScript Technology Private Limited.

The API allows users to register, log in, and then perform CRUD operations on books and authors, as well as manage book borrowing and returns.

## Features

* **Authentication:** Secure user registration and JWT-based login.
* **Author Management:** Full CRUD operations for authors.
* **Book Management:** Full CRUD operations for books, including search and filtering by availability.
* **Borrowing System:** Endpoints to borrow a book (which updates its availability) and return a book.
* **Borrowing History:** A protected endpoint for users to view their personal borrowing history.

## Technology Stack

* **Framework:** **FastAPI**
* **Database:** **SQLite** (for simplicity and quick setup)
* **ORM:** **SQLAlchemy** (for database models and querying)
* **Data Validation:** **Pydantic** (for request/response schemas)
* **Authentication:** **JWT** (using `python-jose` for tokens and `passlib` for password hashing)
* **Server:** **Uvicorn**
* **Environment Variables:** `pydantic-settings`

## 🚀 Setup and Installation

Here is how to set up and run the project locally.

**1. Clone the Repository:**
```bash
git clone [https://github.com/](https://github.com/)[Your_GitHub_Username]/[Your_Repo_Name].git
cd [Your_Repo_Name]
```

**2. Create a Virtual Environment:**
```bash
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

**3. Install Dependencies:**
```bash
pip install -r requirements.txt
```

**4. Set Up Environment Variables:**
Create a `.env` file in the project root by copying the example:
```bash
cp .env.example .env
```
Now, open the `.env` file and add a strong `SECRET_KEY`. You can generate one using:
```bash
python -c 'import secrets; print(secrets.token_hex(32))'
```
Your `.env` file should look like this:
```
SECRET_KEY=your_generated_32_byte_hex_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**5. Run the Application:**
```bash
uvicorn app.main:app --reload
```
The API will be live at `http://127.0.0.1:8000`.

**6. Access the Documentation:**
You can access the interactive Swagger UI documentation at:
**`http://127.0.0.1:8000/docs`**

## 📁 Project Structure

The project uses a modular structure for clear separation of concerns.

```
/app
|-- /api        # API-specific code
|   |-- /v1     # Version 1 of the API
|   |   |-- /endpoints  # Routers for each feature (auth, books, etc.)
|   |   |-- api.py      # Main v1 router
|   |   |-- deps.py     # Dependency injection (e.g., get_current_user)
|-- /core       # Core logic (config, security)
|-- /db         # Database setup (models, session)
|-- /schemas    # Pydantic schemas
|-- main.py     # Main FastAPI app instance
```

## 📋 Example API Calls

You can use `curl` or any API client like Postman. **Note:** You must get a `TOKEN` from the login endpoint and use it as a Bearer token for all protected routes.

**1. Register a New User:**
```bash
curl -X POST "http