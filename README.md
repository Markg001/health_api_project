# Health API Project

This is a full-stack mini project that creates a basic **Health Program Management System** using **FastAPI** (backend) and **HTML/CSS/JavaScript** (frontend).

## Backend Setup (FastAPI + SQLite)

### 1. Create and Activate Virtual Environment (venv)
To isolate dependencies, a virtual environment was created:
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
.\venv\Scripts\activate   # On Windows
```

### 2. Install Python Modules
All necessary Python modules were installed and saved in `requirements.txt`.  
(You can find all modules used there for easy installation.)

Example modules installed:
```bash
pip install fastapi uvicorn sqlalchemy
```

### 3. Backend Files Structure
- `main.py`:  
  Creates the web API and defines routes like:
  - `POST /program/` — Add a new program
  - `POST /clients/` — Add a new client  
  It **uses `models.py` and `schemas.py`** to define how data is stored and validated.

- `models.py`:  
  Tells the application:  
  > "A client has a name, email, and belongs to a program."  
  It defines the **SQLAlchemy ORM models** for the database.

- `database.py`:  
  Connects to the actual database (**SQLite**) so that data can be saved, retrieved, and managed.

- `schemas.py`:  
  Defines **Pydantic models** to tell FastAPI:  
  > "When someone sends us data, this is what it should look like."  
  It helps with request validation and response formatting.

### 4. Running the Backend Server

Installed `uvicorn`, a lightweight ASGI server used to run FastAPI apps:
```bash
pip install uvicorn
```

To start the server, used the following command:
```bash
uvicorn main:app --reload
```
![Image](https://github.com/user-attachments/assets/e9150d05-c862-40b0-a720-f04c5397048c)
- `main:app` means → go to `main.py` and find the FastAPI app instance named `app`.
- `--reload` means → the server automatically reloads when you make code changes (good for development).

### 5. Testing the API

After running the server, it provided a link like:
```
http://127.0.0.1:8000
```

By adding `/docs`, FastAPI automatically provided Swagger UI to test the API visually:
```
http://127.0.0.1:8000/docs
```

Using Swagger UI, clients and programs were added successfully, and corrections were made where needed.

---
![Image](https://github.com/user-attachments/assets/f77e931a-1e43-453a-a37a-3dfde9b8fe0e)

## Frontend Setup (HTML, CSS, JavaScript)

### 1. Frontend Folder
A new folder was created inside the `health_api_project` repository for the frontend files.

### 2. Frontend Files Structure

- `index.html`:  
  The main homepage that links to all other pages.

- `create_client.html`:  
  Page for creating new clients.

- `create_program.html`:  
  Page for creating new programs.

- `enroll.html`:  
  Page for enrolling clients into programs.

- `view_client.html`:  
  Page for searching and viewing client profiles.

- `styles.css`:  
  For basic page styling and making the interface user-friendly.

- `scripts.js`:  
  JavaScript file responsible for communicating with the backend API.  
  It handles:
  - Fetching data
  - Sending form submissions
  - Searching and displaying client profiles dynamically

---
![Image](https://github.com/user-attachments/assets/2b31e231-0ec0-45f3-a4e4-f331dde4a619)

## Summary of Process

1. Set up virtual environment and installed backend dependencies.  
2. Built FastAPI backend with endpoints to manage clients and programs.  
3. Ran server with `uvicorn` and tested with Swagger UI.  
4. Created a clean frontend with HTML, CSS, and JavaScript.  
5. Linked the frontend and backend to work together seamlessly.

---

## How to Run the Project

1. Clone the repository:
```bash
git clone <repository-url>
```

2. Navigate into the backend folder and activate the virtual environment:
```bash
cd health_api_project
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the backend server:
```bash
uvicorn main:app --reload
```

5. Open the frontend files (HTML) directly in a browser and interact with the API.

---

















