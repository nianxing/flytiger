from flask import Blueprint, render_template, current_app

# Create products blueprint
products_bp = Blueprint('products', __name__, url_prefix='/products')

# Example product data - in a real app, this would come from a database or Azure Table
PRODUCTS = [
    {
        'id': 1,
        'name': '天鹰砂纸-P80',
        'description': '适用于木材粗磨、金属表面除锈',
        'specifications': '230mm x 280mm',
        'price': 8.5,
        'image': 'eagle_p80.jpg'
    },
    {
        'id': 2,
        'name': '天鹰砂纸-P120',
        'description': '适用于木材中磨、金属表面磨光',
        'specifications': '230mm x 280mm',
        'price': 8.0,
        'image': 'eagle_p120.jpg'
    },
    {
        'id': 3,
        'name': '天鹰砂纸-P180',
        'description': '适用于木材细磨、涂层磨平',
        'specifications': '230mm x 280mm',
        'price': 7.5,
        'image': 'eagle_p180.jpg'
    },
    {
        'id': 4,
        'name': '天鹰砂纸-P240',
        'description': '适用于精细打磨、上漆前处理',
        'specifications': '230mm x 280mm',
        'price': 7.0,
        'image': 'eagle_p240.jpg'
    },
    {
        'id': 5,
        'name': '天鹰砂纸-水砂纸P1000',
        'description': '适用于汽车漆面打磨、精细工艺',
        'specifications': '230mm x 280mm',
        'price': 9.5,
        'image': 'eagle_water_p1000.jpg'
    }
]

@products_bp.route('/')
def index():
    """Product listing page"""
    return render_template('products/index.html', title='产品列表', products=PRODUCTS)

@products_bp.route('/<int:product_id>')
def detail(product_id):
    """Product detail page"""
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return render_template('errors/404.html'), 404
    
    return render_template('products/detail.html', product=product) 