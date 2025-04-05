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

# Create and activate virtual environment
echo "Setting up Python virtual environment"
python -m venv $DEPLOYMENT_TARGET/env
source $DEPLOYMENT_TARGET/env/bin/activate

# Install dependencies
echo "Installing dependencies"
pip install --upgrade pip
pip install -r $DEPLOYMENT_TARGET/requirements.txt

# Make startup script executable
echo "Making gunicorn startup script executable"
chmod +x $DEPLOYMENT_TARGET/startup.sh

echo "Deployment completed successfully"
exit 0 