from flask import Blueprint, render_template

products_bp = Blueprint('products', __name__, url_prefix='/products')

@products_bp.route('/')
def index():
    return render_template('products/index.html', title='产品列表')

@products_bp.route('/<product_id>')
def detail(product_id):
    return render_template('products/detail.html', title='产品详情', product_id=product_id) 