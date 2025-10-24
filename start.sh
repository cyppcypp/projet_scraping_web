#!/bin/bash

echo "Starting TripAdvisor Dashboard..."

cd scraping_tripadvisor/affichage

if [ -z "$PORT" ]; then
    export PORT=5000
fi

export FLASK_PORT=$PORT

gunicorn --bind 0.0.0.0:$PORT --workers 2 app:app
