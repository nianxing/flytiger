#!/bin/bash

# Navigate to app directory
cd $HOME/site/wwwroot

# Activate virtual environment
source env/bin/activate

# Install dependencies if not already installed
pip install --upgrade pip
pip install -r requirements.txt

# Get the assigned port from Azure or default to 8000
export PORT=${PORT:-8000}
echo "Starting application on port $PORT"

# Start the Flask application with gunicorn
exec gunicorn --bind=0.0.0.0:$PORT run:app 