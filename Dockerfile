# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Install PostgreSQL dependencies (to build psycopg2)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc

# Copy the current directory contents into the container at /app
COPY . /app/

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose port 8000 for Django app
EXPOSE 8000

# Set environment variables
ENV DB_HOST=db

# Run database migrations and start the Django application
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000
