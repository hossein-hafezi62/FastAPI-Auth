# FastAPI Authentication

A simple authentication API built with Python and FastAPI.

## Technologies

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- pwdlib
- python-jose
- Uvicorn

## Features

- User registration
- User login
- Password hashing
- JWT authentication
- Protected routes

## Installation

Create and activate a virtual environment, then install the required packages:

    pip install -r requirements.txt

## Run

Start the FastAPI development server with:

    uvicorn main:app --reload

The API will be available at:

    http://127.0.0.1:8000

Interactive API documentation is available at:

    http://127.0.0.1:8000/docs