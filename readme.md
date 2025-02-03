
# Bookstore Management System API

## Project Overview
This is a RESTful API for managing a bookstore, built using Django REST Framework (DRF) and PostgreSQL.
The API includes features like book management, author management, customer reviews, authentication, pagination, filtering, and search.

## Features
- Token-based authentication
- CRUD operations for books and authors (Admin only)
- Customers can submit their reviews for purchased books
- Pagination, filtering, and search functionality
- Secure endpoints with permissions

## Installation
1. Clone the repository:
   
   git clone <your-repo-url>
   cd Bookstore_Management_System_API
   
2. Create a virtual environment and activate it:
   
   python3 -m venv env1
   source env1/bin/activate  # On Windows: env1\Scripts\activate
   
3. Install dependencies:
   
   pip install -r requirements.txt
   
4. Set up the database:
   
   python manage.py makemigrations
   python manage.py migrate
   
5. Create a superuser:
   
   python manage.py createsuperuser
   
6. Run the server:
   
   python manage.py runserver
   

## Authentication
- The API uses **Token Authentication**.
- Obtain a token by sending a `POST` request to `/api/token/` with valid credentials.

