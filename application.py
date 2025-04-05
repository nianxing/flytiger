# Application entry point for Azure App Service
import os

# Try to install missing dependencies first
try:
    import sys
    import subprocess
    print("Checking for missing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])
    print("Dependencies installed successfully")
except Exception as e:
    print(f"Warning: Could not install dependencies: {str(e)}")

# First try to import everything from run.py
try:
    # Import everything from run.py
    from run import app
    print("Successfully imported app from run.py")
except ImportError as e:
    print(f"Error importing from run.py: {str(e)}")
    # If run.py doesn't work, create a basic Flask app
    try:
        from flask import Flask
        app = Flask(__name__)
        
        @app.route('/')
        def index():
            return "Flask application is running, but could not import original app."
        
        print("Created basic fallback Flask app")
    except Exception as e:
        print(f"Critical error creating fallback app: {str(e)}")

# Make sure app is directly accessible for gunicorn
if 'app' not in globals():
    raise ImportError("Could not import or create Flask app")

# This file is the default entry point expected by Azure App Service
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port) 