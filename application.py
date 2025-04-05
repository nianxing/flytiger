# Import the Flask app from run.py
from run import app as application

# For compatibility with various WSGI servers
app = application

# This file is the default entry point expected by Azure App Service
if __name__ == '__main__':
    app.run() 