from flask import Blueprint, render_template, send_from_directory, Response, request, g
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    lang = g.lang
    company_name = "Flytiger Technology" if lang == 'en' else "飞虎科技"
    product_line = "Eagle Sandpaper" if lang == 'en' else "天鹰砂纸"
    return render_template('index.html', title=f'{company_name} - {product_line}', company_name=company_name, product_line=product_line)

@main_bp.route('/about')
def about():
    lang = g.lang
    title = "About Us" if lang == 'en' else "关于我们"
    return render_template('about.html', title=title)

@main_bp.route('/contact')
def contact():
    lang = g.lang
    title = "Contact Us" if lang == 'en' else "联系我们"
    return render_template('contact.html', title=title)

@main_bp.route('/robots.txt')
def robots():
    return Response("User-agent: *\nDisallow: /admin/\n", mimetype="text/plain")

@main_bp.route('/robots933456.txt')
def azure_probe():
    # This is an Azure health check endpoint
    return Response("", mimetype="text/plain") 