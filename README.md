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
- `web`: Django application service (Gunicorn-ready in `dockerfile`; currently started with `runserver` in `docker-compose.yml`).
- `nginx`: Reverse proxy in front of the Django service.

## Prerequisites

- Docker
- Docker Compose

## Installation and Setup

1. Build and start all services:

```bash
docker compose up -d --build
```

2. Apply database migrations:

```bash
docker compose exec web python manage.py migrate
```

3. Create an admin user:

```bash
docker compose exec web python manage.py createsuperuser
```

4. Collect static files:

```bash
docker compose exec web python manage.py collectstatic --noinput
```

## Access

- Through Nginx: `http://localhost`
- Directly to Django app: `http://localhost:8000`
- Django admin: `http://localhost/admin` or `http://localhost:8000/admin`

## Environment Variables

### Database container (`db`)

- `MYSQL_DATABASE=innovafix_db`
- `MYSQL_USER=user_admin`
- `MYSQL_PASSWORD=password123`
- `MYSQL_ROOT_PASSWORD=root_password`

### Django container (`web`)

- `DB_NAME=innovafix_db`
- `DB_USER=user_admin`
- `DB_PASS=password123`
- `DB_HOST=db`
- `DB_PORT=3306`

## Project Structure

```text
innovafix/
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
# InnovaFix
