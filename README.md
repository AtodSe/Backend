# MyDong Backend Server
REST API server hosting `Bahoo` service.
The Project is written in `Python` and is based on `Django` and `Django Rest Framework`


# Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

The project is Dockerized

## Prerequisites

- Python 3.9+
- Django
- Django Rest Framework
- Docker


## Installing for Development

After cloning the project we setup a virtual environment and install dependencies

```sh
$ python3 -m venv .venv
$ source .venv/bin/activate
$ python install -r requirements/dev.txt
$ touch .env # add required environment variables here
$ docker run -p 5432:5432 --env-file .env --name postgre -h db -d postgres:14.2-alpine
$ docker/docker-entrypoint.sh --migrate python manage.py runserver
```

## Running the Server

```sh
$ docker compose -f docker/docker-compose.yml -p bahoo up -d
```


# Project structure                                                     

```
Bahoo
├── docker
│   ├── docker-compose.yml
│   ├── docker-entrypoint.sh
│   └── Dockerfile
├── api
│   ├── authentication
│   ├── invoice
│   └── users
├── core
│   ├── asgi.py
│   ├── exception_handler.py
│   ├── models.py
│   ├── renderer.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── requirements
│   ├── common.txt
│   ├── dev.txt
│   └── prod.txt
├── manage.py
└── README.md
```

The `docker/` directory is where are the configuration files needed to run the application with docker.

The `core/` contains The configuration root of the project, where project-wide settings, `urls.py`, `renderer.py`, `exception_handler.py`, `models.py` and `wsgi.py` modules are placed.

The `api/` contains Django applications which are `authentication`, `invoice` and `users`

| Api               | Purpose       |
| ----------------- | ------------- |
| `authentication`  | Used for user registration, authentication and refreshing JWT tokens|
| `invoice`         | Manages user invoices, each invoices holds multiple transactions and reminders|
| `users`           | Customizes `User` model |


# Built With

- [Django](https://www.djangoproject.com) - The web framework
- [Django Rest Framework](https://www.django-rest-framework.org) - The REST frame work
- [PostgresSQL](https://www.postgresql.org) - Database
- [Adminer](https://www.adminer.org) - Database Manager

# Authors

- **Mohamad Amin Jafari** - *Initial work* - [Shorakie](https://github.com/Shorakie)


# License

This project is licensed under the `TBD` License - see the [LICENSE.md](LICENSE.md) file for details.
