#!/bin/sh
# Wait for db to be ready (optional loop here)
echo "Applying database migrations..."
python manage.py migrate

echo "Starting server..."
exec "$@"