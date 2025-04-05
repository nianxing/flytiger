# Import everything from run.py
from run import *

# Make sure app is directly accessible for gunicorn
if 'app' not in globals():
    from run import app

# This file is the default entry point expected by Azure App Service
if __name__ == '__main__':
    app.run() 