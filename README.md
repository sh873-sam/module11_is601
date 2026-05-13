# Module 11 FastAPI Calculator API

## Project Overview
Brief description of the FastAPI calculator API with PostgreSQL, Docker, pytest, and CI/CD.

## Features
- Add
- Subtract
- Multiply
- Divide
- Store calculations in PostgreSQL
- REST API with FastAPI
- Swagger documentation
- Docker containerization
- Automated testing with pytest
- GitHub Actions CI/CD pipeline

## Technologies Used
- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker
- Pytest
- Playwright
- GitHub Actions

## Installation

### Clone Repository
```bash
git clone https://github.com/sh873-sam/module11_is601.git
cd module11_is601

Run with Docker
docker compose up --build
API Documentation

Swagger UI:

http://localhost:8000/docs
Running Tests
docker exec -it module11_fastapi_calculator pytest
Docker Services
FastAPI Application
PostgreSQL Database
pgAdmin
CI/CD Pipeline

GitHub Actions automatically:

Runs tests
Performs security stage
Runs deploy stage
Project Structure
app/
tests/
.github/workflows/
docker-compose.yml
Dockerfile
requirements.txt
README.md
