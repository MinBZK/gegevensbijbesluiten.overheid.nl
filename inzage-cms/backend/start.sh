#! /usr/bin/env bash

# Run migrations
alembic -c alembic/alembic.ini upgrade head

# Start the backend server
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-config=app/logging.conf