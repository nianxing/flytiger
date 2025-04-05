"""
This is the application startup file for Azure App Service
"""
import os
from app import app

# Application factory function
def create_app():
    return app

# Get the app instance
application = create_app()

# Define the WSGI application callable
app = application  # For WSGI servers expecting 'app'

if __name__ == "__main__":
    # Get port from environment variable or default to 8000
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port) 