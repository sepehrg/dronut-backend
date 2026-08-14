# Dronut backend

A Django REST API for managing donuts. It uses PostgreSQL and exposes its API under `/api/`.

## Prerequisites

The recommended workflow requires:

- Docker and Docker Compose

To run without Docker, install Python 3.13+ and a running PostgreSQL instance.

## Configure environment variables

Create a `.env` file in the project root. Docker Compose loads this file automatically.

```env
POSTGRES_DB=dronut
POSTGRES_USER=dronut
POSTGRES_PASSWORD=change-me
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

`POSTGRES_HOST` must be `db` when the API runs in Docker. For a locally run API, use `localhost` instead.

## Run with Docker

Build and start the API and database:

```bash
docker compose up --build
```

In a second terminal, apply the database migrations:

```bash
docker compose exec api python manage.py migrate
```

The API is then available at [http://localhost:8000/api/donuts/](http://localhost:8000/api/donuts/). Django's admin is at [http://localhost:8000/admin/](http://localhost:8000/admin/).

Useful Docker commands:

```bash
# Run the test suite
docker compose exec api python manage.py test

# Create an admin user
docker compose exec api python manage.py createsuperuser

# Stop the services (keeps database data)
docker compose down
```

To also remove the persisted PostgreSQL data, run `docker compose down -v`.

## Run locally (without Docker)

1. Start PostgreSQL and create a database/user matching `.env`.
2. Set `POSTGRES_HOST=localhost` in `.env`.
3. Create and activate a virtual environment, then install dependencies:

   ```bash
   python3.13 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

4. Apply migrations and start the server:

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

5. Run tests when needed:

   ```bash
   python manage.py test
   ```

## API

The `donuts` resource supports Django REST Framework's standard CRUD operations:

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/api/donuts/` | List donuts |
| `POST` | `/api/donuts/` | Create a donut |
| `GET` | `/api/donuts/<id>/` | Retrieve a donut |
| `PUT` / `PATCH` | `/api/donuts/<id>/` | Update a donut |
| `DELETE` | `/api/donuts/<id>/` | Delete a donut |

To search by name or description, provide the `query` parameter:

```text
GET /api/donuts/?query=chocolate
```

Example create request:

```bash
curl -X POST http://localhost:8000/api/donuts/ \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Chocolate donut",
    "code": "CHOCOLATE-01",
    "description": "A chocolate glazed donut",
    "price": "3.50",
    "is_available": true
  }'
```

Each donut has `name`, `code` (unique), `description`, `price`, and `is_available` fields.
