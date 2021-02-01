# FastAPI + Tortoise + Aerich + Traefik + Docker.

Quick example of FastAPI with Tortoise and Aerich.

## Requirements

* [Docker](https://www.docker.com/).
* [Docker Compose](https://docs.docker.com/compose/install/).
* [Poetry](https://python-poetry.org/)

## Quick Start
Rename `env_template -> .env` and edit.
```
docker-compose up -d --build
```

Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://app.localhost/api/v1/docs/

Alternative automatic documentation with ReDoc (from the OpenAPI backend): http://app.localhost/api/v1/redoc/

Traefik UI, to see how the routes are being handled by the proxy: http://localhost:8080

Create the first migration and apply it to the database:

```
docker-compose exec app aerich init-db
```

## Create Migration

Make a change to the model. Then, run:

```
docker-compose exec app aerich migrate
docker-compose exec app aerich upgrade
```