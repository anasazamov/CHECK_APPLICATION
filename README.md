# CHECK_APPLICATION

## Django Project Setup Guide

This project is built using **Django** and utilizes **Celery**, **Celery Worker**, and **Celery Beat** for task management. The database used is **PostgreSQL**, and environment variables are managed using `.env` files. Follow the steps below to set up and run the project successfully.

---

## Requirements

- Python 3.9 or higher
- PostgreSQL 13 or higher
- Redis (used as a broker for Celery)
- `virtualenv` (recommended)
- Git (to clone the project repository)

---

## Installation Instructions

### 1. Clone the Project Repository

Download the project by running:

```bash
git clone git@github.com:anasazamov/CHECK_APPLICATION.git
cd CHECK_APPLICATION
```
## Set Up a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  
```
Install the required dependencies:
```bash
pip install -r requirements.txt
```
## Configure the Database
Set up a PostgreSQL database:
```sql
CREATE DATABASE your_db_name;
CREATE USER your_db_user WITH PASSWORD 'your_db_password';
GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_db_user;

```
## Create the .env File
In the root directory of the project, create a .env file and add the following variables:

```env
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PWD=your_db_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your_django_secret_key
TELEGRAM_BOT_TOKEN=telegram_bot_token
```
Replace your_db_name, your_db_user, your_db_password, and your_django_secret_key with your actual values.
## Apply Database Migrations
Run the following commands to prepare the database schema:
```bash
python manage.py makemigrations
python manage.py migrate
```
## Create a Superuser
Set up an admin account for the Django admin panel:
```bash
python manage.py createsuperuser
```
Follow the prompts to complete the setup

## Set Up Celery and Celery Beat
Start the Redis server (if not already running):
```bash
redis-server
```
Start the Celery Worker:
```bash
celery -A core worker --loglevel=info
```
Start the Celery Beat scheduler:
```bash
celery -A core beat --loglevel=info
```
## Run the Django Development Server
```bash
python manage.py runserver
```
## Usage
Access the application by opening http://127.0.0.1:8000 in your browser. Use the admin credentials you created to log in to the admin panel.
## Notes
1. Ensure the Redis server is running before starting Celery.
2. Update DEBUG, database settings, and secret keys for production environments.
3. For deployment, consider using a web server like Gunicorn or uWSGI and a reverse proxy like Nginx.


