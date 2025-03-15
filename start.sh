#!/bin/bash
# Start Uvicorn in the background
uvicorn app:app --host 0.0.0.0 --port 8000 &

# Start Nginx in the foreground (to keep the container running)
nginx -g 'daemon off;'