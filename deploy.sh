#!/bin/bash

# Print deployment info
echo "Starting deployment script"
echo "Current directory: $(pwd)"
echo "Files in current directory:"
ls -la

# Set deployment target if not set
if [ -z "$DEPLOYMENT_TARGET" ]; then
    export DEPLOYMENT_TARGET="$HOME/site/wwwroot"
    echo "DEPLOYMENT_TARGET set to $DEPLOYMENT_TARGET"
fi

echo "Deployment target contents:"
ls -la $DEPLOYMENT_TARGET || echo "Could not list deployment target"

# Create and activate virtual environment
echo "Setting up Python virtual environment"
python -m venv $DEPLOYMENT_TARGET/env || echo "Failed to create virtual environment, continuing..."

# Check if activation script exists
if [ -f "$DEPLOYMENT_TARGET/env/bin/activate" ]; then
    echo "Activating virtual environment"
    source $DEPLOYMENT_TARGET/env/bin/activate
    echo "Python version: $(python --version)"
else
    echo "Warning: Virtual environment activation script not found"
fi

# Install dependencies
echo "Installing dependencies"
pip install --upgrade pip
pip install -r $DEPLOYMENT_TARGET/requirements.txt

# Make startup script executable
echo "Making startup script executable"
chmod +x $DEPLOYMENT_TARGET/startup.sh

# Create a simple test file to verify deployment
echo "Creating test file"
echo "Deployment was successful on $(date)" > $DEPLOYMENT_TARGET/deployment_info.txt

# Create necessary directories if they don't exist
echo "Creating log directories"
mkdir -p $HOME/LogFiles

echo "Deployment completed successfully"
exit 0 