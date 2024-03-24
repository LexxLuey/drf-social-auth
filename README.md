# Django Rest Framework API Setup Guide

This guide provides step-by-step instructions to set up the Django Rest Framework API project locally. 

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Setup](#local-setup)
3. [Docker Setup](#docker-setup)

## Prerequisites
Since there are two ways you can setup this project, this section is divided into two for the local (non docker) setup and docker setup.

### Local Setup Prerequisites
Before you begin, make sure you have the following installed:

- Python (3.10 or later)
- Poetry or pip (Python package manager)
- PostgreSQL
- Redis
- (Optional) Google OAuth Client Key ([https://console.cloud.google.com/](https://console.cloud.google.com/))
- (Optional) Apple Developer Account and keys ([https://docs.allauth.org/en/latest/socialaccount/providers/apple.html](https://docs.allauth.org/en/latest/socialaccount/providers/apple.html))


### Docker Setup Prerequisites
Before you begin, make sure you have the following installed:

- Docker
- Docker-Compose
- (Optional) Google OAuth Client Key ([https://console.cloud.google.com/](https://console.cloud.google.com/))
- (Optional) Apple Developer Account and keys ([https://docs.allauth.org/en/latest/socialaccount/providers/apple.html](https://docs.allauth.org/en/latest/socialaccount/providers/apple.html))

## Local Setup (Using a command line terminal)

1. Clone the project.
```bash
git clone https://github.com/LexxLuey/drf-social-auth/
```

2. Enter the cloned projects directory
```bash
cd drf-social-auth
```

3. Create a virtual environment, activate it and install dependencies using either pip or poetry:

```bash title="using pip"
python3 -m venv venv
source venv/bin/activate  
# On Windows: 
# venv\Scripts\activate

pip install -r requirements.dev.txt
```

```bash title="using poetry"
poetry install
poetry shell
```

4. Create a PostgreSQL database

5. Create .env file with variables like the ones in the .env.sample file.

6. Get a Google OAuth keys for your app.

7. Get an Apple OAuth keys for your app.

8. Update the .env file with your database credentials, google and apple oauth keys.


9. Apply migrations:

```bash

python manage.py migrate
```

10. Run the Django development server:

```bash

python manage.py runserver
```

11. Access the Django API at [8000](http://localhost:8000)

### Running Tests

12. (OPTIONAL) Run tests by doing:
```bash
python manage.py test cinema.test
```
### Starting Celery workers

13. Start the worker using the following command in a new terminal.
```bash
celery -A core worker -l info
```

14. Start the beat by running the following command in a new terminal 
```bash
celery -A core beat -l info
```

NOTE: Please update the `id_token` and `access_tokens` with actual values gotten from google oauth playground and apple oauth playground appropriately whenever testing accounts app.


## Docker Setup 

This repository contains a Django web application configured to run with Docker using Docker Compose. It includes services for Django, PostgreSQL, Redis, Celery worker, and Celery beat.

## Prerequisites

Make sure you have Docker and Docker Compose installed on your system.

## Setup

1. Clone this repository:

```bash
git clone https://github.com/LexxLuey/drf-social-auth/
cd drf-social-auth
```

2. Create a `.env` file in the project root directory and add your environment variables:

```bash
DEBUG=1
SECRET_KEY=your_secret_key
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=db
DB_PORT=5432
REDIS_HOST=redis
REDIS_PORT=6379
```

3. If it is your **FIRST** time of running this app, **DO THIS** otherwise you can skip to next step: 

```bash
docker-compose up db # Wait until you see 'database system is ready to accept connections'
docker-compose up redis # Wait until you see 'Ready to accept connections'
docker-compose up
```
run each command in a separate terminal.

4. Get docker containers up and running: 

```bash
docker-compose up
```

5. Access the application at `http://localhost:8000`.

### Running Commands

You can run Django management commands and Celery tasks using Docker Compose.

#### Django Management Commands

To run Django management commands, use the `docker-compose exec` command. For example, to create migrations:

```bash
docker-compose exec web python manage.py makemigrations
```

### API Tests

To run tests, use the `docker-compose exec` command as well. For example, to start testing the cinema app:

```bash
docker-compose exec web python manage.py test cinema.tests
```


---

# TODO

- Make docker image of app slimmer by reducing number of layers
- Integrate authentication into cinema app
- Image and File storage to third party service such s3, cloudinary etc
