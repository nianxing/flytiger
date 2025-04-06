# Application entry point for Azure App Service
import os
import sys

# Add current directory to path to ensure imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Debug information
print("=== Application Startup ===")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Files in current directory:")
for file in os.listdir('.'):
    print(f"  - {file}")
if os.path.exists('app'):
    print("App directory exists, contains:")
    for file in os.listdir('app'):
        print(f"  - app/{file}")
print("===========================")

# Try to install missing dependencies first
try:
    import subprocess
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Dependencies installed successfully")
except Exception as e:
    print(f"Warning: Could not install dependencies: {str(e)}")

# First try to import Flask
try:
    from flask import Flask, render_template
    print("Successfully imported Flask")
except ImportError as e:
    print(f"CRITICAL ERROR: Could not import Flask: {str(e)}")
    sys.exit(1)

# Try to import from config
try:
    from config import current_config
    print("Successfully imported configuration")
except ImportError as e:
    print(f"Error importing config: {str(e)}")
    # Create a basic configuration
    print("Creating basic configuration")
    class BasicConfig:
        SECRET_KEY = os.environ.get('SECRET_KEY', 'basic-key')
        DEBUG = False
    current_config = BasicConfig()

# Try to import the app from run.py
try:
    from run import app
    print("Successfully imported app from run.py")
except ImportError as e:
    print(f"Error importing from run.py: {str(e)}")
    print("Trying to create app directly...")
    
    # Try to import create_app from app module
    try:
        from app import create_app
        print("Found create_app function, creating app...")
        app = create_app(current_config)
        print("Successfully created app using create_app")
    except ImportError as e:
        print(f"Error importing create_app: {str(e)}")
        # Create a basic Flask app
        try:
            print("Creating basic fallback Flask app")
            app = Flask(__name__)
            app.config.from_object(current_config)
            
            @app.route('/')
            def index():
                return "Flask application is running with minimal configuration. Could not import original app."
            
            @app.route('/debug')
            def debug():
                html = "<h1>Debug Information</h1>"
                html += "<h2>Environment</h2>"
                html += "<ul>"
                html += f"<li>Python version: {sys.version}</li>"
                html += f"<li>Working directory: {os.getcwd()}</li>"
                html += f"<li>PYTHONPATH: {os.environ.get('PYTHONPATH', 'Not set')}</li>"
                html += "</ul>"
                
                html += "<h2>Files</h2>"
                html += "<ul>"
                for file in os.listdir('.'):
                    html += f"<li>{file}</li>"
                html += "</ul>"
                
                html += "<h2>Sys.path</h2>"
                html += "<ul>"
                for path in sys.path:
                    html += f"<li>{path}</li>"
                html += "</ul>"
                
                return html
            
        except Exception as e:
            print(f"Critical error creating fallback app: {str(e)}")
            sys.exit(1)

# Make sure app is directly accessible for gunicorn
if 'app' not in globals():
    raise ImportError("Could not import or create Flask app")

# This file is the default entry point expected by Azure App Service
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port) 