# Innovafix

Innovafix is a web-based inventory and supplier management platform built with Django. It helps teams manage suppliers, product intakes, sales, clients, users, roles, equipment maintenance, and reporting workflows from a single interface.

## Tech Stack

- Django 5.x
- MySQL 8.0
- Docker and Docker Compose
- Nginx (reverse proxy)
- Jazzmin (Django admin theme)

## Architecture

The project runs in three containers:

- `db`: MySQL 8.0 database service.
- `web`: Django application service.
- `nginx`: Reverse proxy in front of the Django service.

## Prerequisites

- Docker
- Docker Compose

## Installation and Setup

1. Create your local environment file:

```bash
cp .env.example .env
```

2. Edit `.env` and replace every placeholder secret with your own values.

3. Build and start all services:

```bash
docker compose up -d --build
```

4. Apply database migrations:

```bash
docker compose exec web python manage.py migrate
```

5. Create an admin user:

```bash
docker compose exec web python manage.py createsuperuser
```

6. Collect static files:

```bash
docker compose exec web python manage.py collectstatic --noinput
```

## Access

- Through Nginx: `http://localhost:8080`
- Directly to Django app: `http://localhost:8000`
- Django admin: `http://localhost:8080/admin` or `http://localhost:8000/admin`

## Environment Variables

Use `.env.example` as the template for local configuration. Do not commit real credentials, secrets, generated static files, or uploaded media files.

## Project Structure

```text
innovafix/
├── .env.example
├── docker-compose.yml
├── dockerfile
├── manage.py
├── requirements.txt
├── nginx/
│   └── default.conf
├── proveedor/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── proveedor_app/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
└── static/
```

## Notes

- If this is your first run, execute setup commands in order.
- If static assets do not update, rerun `collectstatic` and refresh your browser cache.
- Rotate any credentials that were previously committed before publishing the project again.
