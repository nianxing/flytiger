from flask import Blueprint, render_template, current_app, request, g

# Create products blueprint
products_bp = Blueprint('products', __name__, url_prefix='/products')

# Example product data - in a real app, this would come from a database or Azure Table
PRODUCTS = [
    {
        'id': 1,
        'name': {
            'cn': '天鹰砂纸-P80',
            'en': 'Eagle Sandpaper-P80'
        },
        'description': {
            'cn': '适用于木材粗磨、金属表面除锈',
            'en': 'Suitable for rough wood sanding and metal surface rust removal'
        },
        'specifications': '230mm x 280mm',
        'price': 8.5,
        'image': 'eagle_p80.jpg'
    },
    {
        'id': 2,
        'name': {
            'cn': '天鹰砂纸-P120',
            'en': 'Eagle Sandpaper-P120'
        },
        'description': {
            'cn': '适用于木材中磨、金属表面磨光',
            'en': 'Suitable for medium wood sanding and metal surface polishing'
        },
        'specifications': '230mm x 280mm',
        'price': 8.0,
        'image': 'eagle_p120.jpg'
    },
    {
        'id': 3,
        'name': {
            'cn': '天鹰砂纸-P180',
            'en': 'Eagle Sandpaper-P180'
        },
        'description': {
            'cn': '适用于木材细磨、涂层磨平',
            'en': 'Suitable for fine wood sanding and coating leveling'
        },
        'specifications': '230mm x 280mm',
        'price': 7.5,
        'image': 'eagle_p180.jpg'
    },
    {
        'id': 4,
        'name': {
            'cn': '天鹰砂纸-P240',
            'en': 'Eagle Sandpaper-P240'
        },
        'description': {
            'cn': '适用于精细打磨、上漆前处理',
            'en': 'Suitable for fine sanding and pre-painting preparation'
        },
        'specifications': '230mm x 280mm',
        'price': 7.0,
        'image': 'eagle_p240.jpg'
    },
    {
        'id': 5,
        'name': {
            'cn': '天鹰砂纸-水砂纸P1000',
            'en': 'Eagle Sandpaper-Wet P1000'
        },
        'description': {
            'cn': '适用于汽车漆面打磨、精细工艺',
            'en': 'Suitable for automotive paint sanding and fine craftsmanship'
        },
        'specifications': '230mm x 280mm',
        'price': 9.5,
        'image': 'eagle_water_p1000.jpg'
    }
]

@products_bp.route('/')
def index():
    """Product listing page"""
    lang = g.lang
    title = 'Product List' if lang == 'en' else '产品列表'
    
    # 处理产品数据，根据语言选择对应的名称和描述
    products_with_lang = []
    for product in PRODUCTS:
        product_with_lang = product.copy()
        product_with_lang['name'] = product['name'][lang]
        product_with_lang['description'] = product['description'][lang]
        products_with_lang.append(product_with_lang)
    
    return render_template('products/index.html', title=title, products=products_with_lang)

@products_bp.route('/<int:product_id>')
def detail(product_id):
    """Product detail page"""
    lang = g.lang
    
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return render_template('errors/404.html'), 404
    
    # 创建带有语言版本的产品副本
    product_with_lang = product.copy()
    product_with_lang['name'] = product['name'][lang]
    product_with_lang['description'] = product['description'][lang]
    
    return render_template('products/detail.html', product=product_with_lang) 