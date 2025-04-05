# This file provides an alternative WSGI entry point
from application import app as application

# For compatibility with various WSGI servers
app = application

if __name__ == '__main__':
    application.run() 