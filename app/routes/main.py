from flask import Blueprint, render_template

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