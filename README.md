# 🧪 Sr. Python Developer Assignment: Mini Event Management System

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

## Assumptions

- The application uses a SQLite database by default for simplicity. The database file `test.db` will be created in the root directory. This can be configured to use PostgreSQL by setting the `DATABASE_URL` environment variable.
- Timezones are handled as UTC. The input `start_time` and `end_time` are expected to be in ISO 8601 format with timezone information.

## Next Steps (Bonus)

- Implement unit tests using `pytest`.
- Add more robust error handling and logging.
- Use a production-grade database like PostgreSQL.
- Add user authentication and authorization.
- Deploy the application to a cloud provider.
