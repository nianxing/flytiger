#!/bin/bash

# This script is called directly by Azure App Service

echo "================================"
echo "Starting custom startup script"
echo "================================"

# Output environment information for debugging
echo "Environment:"
echo "Python: $(python --version)"
echo "Current directory: $(pwd)"
echo "Directory contents:"
ls -la

# Install required packages directly
echo "Installing requirements..."
pip install --upgrade pip
pip install gunicorn
pip install -r requirements.txt

# Get the assigned port from Azure
export PORT="${PORT:-8000}"
echo "Starting application on port $PORT"

# Try different app entry points
echo "Checking available entry points..."

if [ -f "application.py" ]; then
    echo "Found application.py, starting with it..."
    exec gunicorn --bind=0.0.0.0:$PORT application:app
elif [ -f "app.py" ]; then
    echo "Found app.py, starting with it..."
    exec gunicorn --bind=0.0.0.0:$PORT app:app
elif [ -f "wsgi.py" ]; then
    echo "Found wsgi.py, starting with it..."
    exec gunicorn --bind=0.0.0.0:$PORT wsgi:app
elif [ -f "run.py" ]; then
    echo "Found run.py, starting with it..."
    exec gunicorn --bind=0.0.0.0:$PORT run:app
else
    echo "No recognized entry point found."
    exit 1
fi 