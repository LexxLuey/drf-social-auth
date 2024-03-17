# Django Rest Framework API Setup Guide

This guide provides step-by-step instructions to set up the Django Rest Framework API project locally. 

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Setup](#local-setup)

## Prerequisites

Before you begin, make sure you have the following installed:

- Python (3.10 or later)
- pip (Python package manager)
- PostgreSQL
- Google OAuth Client Key ([https://console.cloud.google.com/](https://console.cloud.google.com/))
- Apple Developer Account and keys ([https://docs.allauth.org/en/latest/socialaccount/providers/apple.html](https://docs.allauth.org/en/latest/socialaccount/providers/apple.html))

## Local Setup

1. Unzip the project and open a terminal console in the root of the unzipped project.

2. Create a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate  
# On Windows: 
# venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.dev.txt
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

12. Run tests by doing:
```bash
python manage.py accounts.test
```
NOTE: Please update the `id_token` and `access_tokens` with actual values gotten from google oauth playground and apple oauth playground appropriately whenever testing.