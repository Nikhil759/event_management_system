![ChatGPT Image Jun 26, 2025, 10_24_44 PM](https://github.com/user-attachments/assets/65825964-c767-4087-a43d-9624fa010c6a)# Assignment: Mini Event Management System

This project is a mini event management system API built with Python, FastAPI, and SQLAlchemy.

## Objective

Build a Mini Event Management System API with a focus on clean architecture, scalability, and data integrity.

## Features

- Create new events with details like name, location, time, and capacity.
- List all upcoming events.
- Register attendees for events, preventing overbooking and duplicate registrations.
- View the list of attendees for a specific event.
- Timezone-aware datetime handling.
- Automatic API documentation with Swagger UI.

## Project Structure

The project follows a clean architecture approach, with a clear separation of concerns:

- `main.py`: The entry point of the application.
- `api/`: Contains the FastAPI routers and endpoints.
- `services/`: Contains the business logic of the application.
- `models/`: Contains the SQLAlchemy models and Pydantic schemas.
- `db/`: Contains the database connection and session management logic.
- `tests/`: Contains the unit tests (to be implemented).


## Tech Stack Rationale

This project follows a clear separation of concerns by using Flask for serving the web-based UI and FastAPI for building structured backend APIs with automatic, interactive documentation. The decision to use both frameworks is intentional — Flask efficiently handles template rendering and UI workflows, while FastAPI provides a modern, standards-compliant foundation for the API layer.

Although the current implementation uses synchronous APIs, adopting FastAPI ensures future scalability, native async support, and built-in features like OpenAPI and Swagger documentation, all of which promote maintainability and extensibility. This separation reflects real-world architectural practices where UI and backend services evolve independently, making the system easier to scale and adapt over time.


## MVC Architecture in This Project

This project follows the Model-View-Controller (MVC) architectural pattern, ensuring a clean separation of concerns and maintainability:

- **Model:**
  - Defined in the `models/` directory (SQLAlchemy models) and `schemas/` (Pydantic schemas).
  - Responsible for representing the database structure, data validation, and business logic.

- **View:**
  - Implemented in the `api/` directory (FastAPI routers for API endpoints) and `flask_ui.py` (Flask web UI for HTML rendering).
  - Handles presentation, user/API input, and output formatting (JSON or HTML).

- **Controller:**
  - Encapsulated in the `services/` directory.
  - Contains the business logic, input validation, and orchestrates interactions between models and views.

This structure makes the codebase modular, scalable, and easy to test or extend. Each layer has a clear responsibility, following best practices for professional backend development.

![ChatGPT Image Jun 26, 2025, 10_24_44 PM](https://github.com/user-attachments/assets/9b0d0724-749d-42c7-8404-7d021bb33425)


## Setup Instructions

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd event_management_system
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
    
    On Windows:
    ```bash
    venv\Scripts\activate
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**

    ```bash
    uvicorn main:app --reload
    ```

    The application will be running at `http://127.0.0.1:8000`.

## API Usage

You can access the interactive API documentation (Swagger UI) at `http://127.0.0.1:8000/docs`.

Here are some example `curl` commands:

### Create an event

```bash
curl -X POST "http://127.0.0.1:8000/events/" -H "Content-Type: application/json" -d '{
  "name": "Tech Conference 2024",
  "location": "San Francisco",
  "start_time": "2024-09-15T09:00:00Z",
  "end_time": "2024-09-15T17:00:00Z",
  "max_capacity": 100
}'
```

### List all upcoming events

```bash
curl -X GET "http://127.0.0.1:8000/events/"
```

### Register for an event

```bash
curl -X POST "http://127.0.0.1:8000/events/1/register" -H "Content-Type: application/json" -d '{
  "name": "John Doe",
  "email": "john.doe@example.com"
}'
```

### Get event attendees

```bash
curl -X GET "http://127.0.0.1:8000/events/1/attendees"
```

### Get a single event with attendees

```bash
curl -X GET "http://127.0.0.1:8000/events/1"
```


## Web UI (Flask)

A simple, modern web UI is included for event management.

### How to Run the Web UI

1. Make sure your virtual environment is activated:
   ```bash
   source venv/bin/activate
   ```
2. Start the Flask UI:
   ```bash
   python flask_ui.py
   ```
   (If you are not in the event_management_system directory, use the full path: `python event_management_system/flask_ui.py`)

3. Open your browser and go to:
   - http://127.0.0.1:5000/
   - or http://localhost:5000/

You will see the Event Management System web interface, where you can create events, register attendees, and view all records.





## Running Unit Tests

This project includes unit tests written with `pytest` to ensure the core API features work as expected.

### What is tested?
- **Event creation:** Verifies that events can be created via the API.
- **Attendee registration:** Checks that attendees can register for events.
- **Duplicate registration prevention:** Ensures the same email cannot register twice for the same event.
- **Event capacity enforcement:** Confirms that no more attendees can register than the event's max capacity.

### How to run the tests
1. Activate your virtual environment:
   ```bash
   source venv/bin/activate
   ```
2. Run the tests using pytest:
   ```bash
   pytest tests/
   ```

You should see output indicating the results of each test. All tests should pass if the application is working correctly.

