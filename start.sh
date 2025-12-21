#!/bin/sh

# Railway startup script to handle PORT environment variable properly
# Default to port 8000 if PORT is not set
PORT=${PORT:-8000}

echo "Starting FalsifyX on port $PORT"

# Start gunicorn with the resolved port
exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 30 --max-requests 50 wsgi_lite:app