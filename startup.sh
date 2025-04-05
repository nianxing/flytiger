#!/bin/bash

# Print debug information
echo "Starting application..."
echo "Current directory: $(pwd)"
echo "Directory contents:"
ls -la

# Navigate to app directory
cd $HOME/site/wwwroot
echo "Changed to app directory: $(pwd)"
echo "App directory contents:"
ls -la

# Check if virtual environment exists
if [ ! -d "env" ]; then
    echo "Creating virtual environment..."
    python -m venv env
fi

# Activate virtual environment
echo "Activating virtual environment..."
source env/bin/activate
echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"

# Install dependencies if not already installed
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check if Flask app exists
if [ ! -f "run.py" ]; then
    echo "ERROR: run.py not found!"
    exit 1
fi

# Get the assigned port from Azure or default to 8000
export PORT=${PORT:-8000}
echo "Starting application on port $PORT"

# Set Flask environment variables
export FLASK_APP=run.py
export FLASK_ENV=production

# Start the Flask application with gunicorn
echo "Launching gunicorn with app:app..."
exec gunicorn --bind=0.0.0.0:$PORT --log-level=debug run:app 