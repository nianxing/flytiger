#!/bin/bash

# Print debug information
echo "Starting application..."
echo "Current directory: $(pwd)"
echo "Directory contents:"
ls -la

# This is needed since Azure is looking for application.py by default
echo "Creating symlink to ensure application.py is found"
if [ ! -f "application.py" ] && [ -f "run.py" ]; then
  cp run.py application.py
fi

# Install gunicorn if not installed
pip install gunicorn

# Get the assigned port from Azure
export PORT="${PORT:-8000}"
echo "Starting application on port $PORT"

# Let Azure handle the startup
echo "Application ready to start..." 