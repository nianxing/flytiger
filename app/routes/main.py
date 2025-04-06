from flask import Blueprint, render_template, send_from_directory, Response
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html', title='飞虎科技 - 天鹰砂纸')

@main_bp.route('/about')
def about():
    return render_template('about.html', title='关于我们')

@main_bp.route('/contact')
def contact():
    return render_template('contact.html', title='联系我们')

@main_bp.route('/robots.txt')
def robots():
    return Response("User-agent: *\nDisallow: /admin/\n", mimetype="text/plain")

@main_bp.route('/robots933456.txt')
def azure_probe():
    # This is an Azure health check endpoint
    return Response("", mimetype="text/plain") 