# MzansiBuilds

MzansiBuilds is a full-stack web application that allows users to create and manage projects, collaborate with others, track milestones and engage through comments and collaboration requests.

The platform is designed to simulate a real-world project collaboration system with authentication, role-based access control and REST API integration.

---

# Architecture Overview
- Frontend communicates with backend via HTTP requests
- Backend exposes REST API endpoints using FastAPI
- Authentication is handled using JWT tokens stored in localStorage
- Role-based access control ensures only project owners can modify their projects
- Database layer managed using SQLAlchemy ORM

---

# Tech Stack

## Backend
- FastAPI (Python)
- SQLAlchemy ORM
- SQLite database
- JWT Authentication (python-jose)
- Password hashing (passlib + argon2)

## Frontend
- HTML5
- CSS3
- JavaScript
- Fetch API for backend communication

---

# Features

## User System
- User registration
- Login with JWT authentication
- View and update profile
- Delete account securely (password required)

## Projects
- Create projects
- View all active projects (Live Feed)
- View completed projects (Celebration Wall)
- Update and delete own projects
- Role-based access (owner vs non-owner)

## Milestones
- Add milestones to projects
- Edit milestones 
- Delete milestones
- View milestones per project

## Comments
- Add comments to projects
- View comments
- Delete comments

## Collaboration System
- Request collaboration on projects
- Prevent duplicate requests
- Project owners can:
  - View requests
  - Accept requests
  - Reject requests
- Users can view their sent requests

---

# How to Run the Project
The backend MUST be running for frontend functionality.
Ensure backend is set up correctly and started before using the UI.

## 1. Clone the Repository (terminal or GitHub desktop)

## 2. Backend Setup using terminal (These instructions can vary depending on how you want to set it up)
- Note: Use the folder name that you clone the repository to on your device e.g. mzansibuilds
- Run the following commands:
  - cd mzansibuilds
  - python -m venv venv (Create the virtual environment if you want to use one, although not necessarily required)
  - venv\Scripts\activate (If using venv)
  - pip install -r requirements.txt (Install dependencies)
  - uvicorn app.main:app --reload (Run the FastAPI server)

- To stop the server, press CTRL + C.
- The backend runs at: http://127.0.0.1:8000
- Swagger UI for testing: http://127.0.0.1:8000/docs

## 3. Frontend Setup (Recommended method - Visual Studio Code)
- Install the extension for viewing html files: Live Preview
- Once installed, open the project in VS Code and navigate to the frontend folder
- Inside is all the frontend files
- To see the UI display, right click on an html file and click "Show Preview"
- The user flow begins at home-page.html

A few quick login test cases to use are:
- User 1: jennyjo
  - Email: jenny@example.com
  - password: passw0RD
- User 2: DannyP123
  - Email: daniel@gmail.com
  - password: DannyCodes
- User 3: NickFox
  - Email: nick@outlook.com
  - Nicko554
