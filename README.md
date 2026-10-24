# Quaver

Quaver is a music library and playlist web application built with Flask and Vue. It includes account roles for listeners, creators, and administrators, plus song and album management.

## Requirements

- Python 3.10 or newer
- Node.js and npm
- Redis, available at `127.0.0.1:6380` (used for caching and Celery)

The Flask app uses SQLite and creates its database and initial roles when started with `python app.py`. The initial administrator account is `admin123` with password `123`; change these defaults before using the app beyond local development.

## Run locally

Open a terminal in the repository root and install the backend dependencies:

```sh
python -m venv .venv
# Windows PowerShell:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

# macOS/Linux:
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Start Redis

Quaver expects Redis at `127.0.0.1:6380`. Redis is a separate service; it does not start with the Flask app.

On Windows, one option is to run Redis in Docker Desktop. In a terminal, start the container with:

```sh
docker run --name quaver-redis -p 6380:6379 -d redis
```

This maps Quaver's port `6380` to Redis's default container port `6379`. If you already created the container earlier, start it with `docker start quaver-redis` instead. To stop it, run `docker stop quaver-redis`.

On macOS with Homebrew, install and start Redis on port `6380`:

```sh
brew install redis
redis-server --port 6380
```

On Linux, install Redis with your distribution's package manager, then run it on port `6380` (for example, `redis-server --port 6380`). Keep the Redis terminal or service running while using Quaver.

## Start the application

With Redis running, start the Flask API in one terminal from the repository root:

```sh
python app.py
```

In a second terminal, install and start the Vue development server:

```sh
cd vue-project
npm install
npm run dev
```

Open the local URL printed by Vite (typically `http://localhost:5173`). The frontend expects the API at `http://localhost:5000/api`.

Email reminders are sent through a local SMTP server on port `1025`. To use the scheduled reminder jobs, run a Celery worker and beat scheduler from the repository root in separate terminals:

```sh
celery -A app.celery_app worker --loglevel=info
celery -A app.celery_app beat --loglevel=info
```

Without a local SMTP server, email sending will fail when reminder jobs run. The core web app does not require the worker or scheduler to be started for ordinary browsing and song management.

## Build the frontend

```sh
cd vue-project
npm run build
```

## Technologies

- Flask, Flask-SQLAlchemy, Flask-Security-Too, and Flask-RESTful
- Vue 3 and Vite
- SQLite, Redis, and Celery

## Credits

Developed by Samyuktha for the Modern Application Development II Project course, under the IIT Madras BS in Data Science and Applications.
