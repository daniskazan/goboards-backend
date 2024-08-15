#!/bin/bash

echo "Apply database migrations"
alembic upgrade head
exec "$@"

echo "Starting server"
python src/main.py