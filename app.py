#!/usr/bin/env python
# Main application file for Azure
import os

# First try to import app from run.py
try:
    from run import app
    print("Imported app from run.py")
except ImportError:
    # If run.py doesn't work, create a basic Flask app
    print("Creating new Flask app")
    from flask import Flask, render_template
    from config import current_config
    
    app = Flask(__name__)
    app.config.from_object(current_config)
    
    @app.route('/')
    def index():
        return render_template('index.html', title='飞虎科技 - 天鹰砂纸')
    
    @app.route('/about')
    def about():
        return render_template('about.html', title='关于我们')

# This is the main entry point for Azure
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port) 