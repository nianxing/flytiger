# Import the Flask app from run.py
from run import app

# This file is the default entry point expected by Azure App Service
if __name__ == '__main__':
    app.run() 