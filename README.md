# Containerized Task Management System
## 1. Project Overview
    This project is a Microservices-based Task Management application designed to demonstrate scalable DevOps architecture. It decouples the user interface, business logic, and background processing into isolated containers, orchestrated via Docker Compose.
    The system allows users to submit tasks which are queued and processed asynchronously by a background worker, ensuring the main application remains responsive even during heavy loads.

## 2. Architecture
    The application consists of 6 Docker containers working in harmony:

    - Nginx (Gateway): The entry point. It acts as a Reverse Proxy, routing traffic to either the Frontend or Backend.

    - Frontend (React): A responsive UI for viewing and adding tasks.

    - Backend (FastAPI): The REST API that handles requests, updates the database, and publishes messages to the queue.

    - PostgreSQL (Database): Persistent storage for task records.

    - RabbitMQ (Message Broker): A queue system to handle asynchronous task processing.

    - Worker (Python): A background service that listens to the queue and performs the actual task processing (simulated heavy work).

## 3. Tech Stack
    - Orchestration: Docker & Docker Compose

    - Frontend: React.js, Node.js 16

    - Backend: Python 3.9, FastAPI, Uvicorn, SQLAlchemy

    - Database: PostgreSQL 13

    - Message Queue: RabbitMQ 3 (Management Plugin enabled)

    - Proxy: Nginx (Alpine Linux)

## 4. Project Structure
The codebase is organized into modular services:

    ```
    task-manager-app/
    ├── backend/                # FastAPI Application
    │   ├── app/
    │   │   ├── main.py         # API Routes & Logic
    │   │   ├── models.py       # Database Tables
    │   │   ├── schemas.py      # Pydantic Validators
    │   │   └── database.py     # DB Connection Logic
    │   ├── Dockerfile
    │   └── requirements.txt
    ├── frontend/               # React Application
    │   ├── src/                # UI Components
    │   ├── Dockerfile
    │   └── package.json
    ├── worker/                 # Background Processor
    │   ├── app/
    │   │   ├── worker.py       # Queue Listener & Logic
    │   │   ├── models.py       # Shared DB Models
    │   │   └── database.py     # Shared DB Connection
    │   ├── Dockerfile
    │   └── requirements.txt
    ├── nginx/                  # Gateway Configuration
    │   ├── nginx.conf          # Routing Rules
    │   └── Dockerfile
    └── docker-compose.yml      # Orchestration Config
    ```

5. Prerequisites & Setup
    Prerequisites
    Docker Desktop must be installed and running.

    Ports 8080 (Web), 5432 (DB), and 5672 (RabbitMQ) should be free.

    Installation Steps
    Clone the Repository (or unzip the project folder).

    Navigate to the root directory:

    Bash
    ```
    cd task-manager-app
    Build and Run the Containers:
    ```

    Bash
    ```
    docker compose up --build
    Wait for all 6 containers to report "Running" in Docker Dashboard.
    ```

6. How to Use
    Accessing the Application
    Open your web browser and navigate to:
   
    http://localhost:8080



Workflow
    Create a Task: Type "Generate Report" in the input box and click Add Task.

    View Status:

    PENDING: The task is saved in Postgres and sent to RabbitMQ.

    PROCESSING: The Worker has picked up the task.

    DONE: The Worker has finished the task (after a 10-second simulated delay).