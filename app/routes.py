from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from app.models import Product, Order
from app.azure_storage import save_order_to_table

# 创建蓝图
main_bp = Blueprint('main', __name__)

# 示例产品数据 - 正式环境可从数据库或Azure Table获取
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

@main_bp.route('/')
def index():
    """首页"""
    company_name = current_app.config['COMPANY_NAME']
    product_line = current_app.config['PRODUCT_LINE']
    return render_template('index.html', company_name=company_name, product_line=product_line)

@main_bp.route('/products')
def products():
    """产品列表页"""
    return render_template('products.html', products=PRODUCTS)

@main_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    """产品详情页"""
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return render_template('errors/404.html'), 404
    return render_template('product_detail.html', product=product)

@main_bp.route('/cart', methods=['GET', 'POST'])
def cart():
    """购物车页面"""
    if request.method == 'POST':
        product_id = int(request.form.get('product_id'))
        quantity = int(request.form.get('quantity', 1))
        
        # 这里应该将商品添加到购物车中（会话或数据库）
        # 简单模拟，实际应用中应使用session或数据库
        flash(f'已添加商品到购物车！')
        return redirect(url_for('main.cart'))
    
    # 模拟购物车中的商品
    cart_items = [
        {'product': PRODUCTS[0], 'quantity': 2},
        {'product': PRODUCTS[2], 'quantity': 1}
    ]
    total = sum(item['product']['price'] * item['quantity'] for item in cart_items)
    
    return render_template('cart.html', cart_items=cart_items, total=total)

@main_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """结账页面"""
    if request.method == 'POST':
        # 处理订单提交
        customer_name = request.form.get('name')
        customer_email = request.form.get('email')
        customer_phone = request.form.get('phone')
        address = request.form.get('address')
        
        # 创建订单对象
        order = Order(
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            address=address,
            total=100.0,  # 实际应从购物车计算
            items=[{
                'product_id': 1,
                'name': '天鹰砂纸-P80',
                'price': 8.5,
                'quantity': 2
            }]  # 实际应从购物车获取
        )
        
        # 保存订单到Azure Table
        try:
            save_order_to_table(order)
            flash('订单已成功提交！')
            return redirect(url_for('main.order_confirmation'))
        except Exception as e:
            flash(f'订单提交失败：{str(e)}')
    
    return render_template('checkout.html')

@main_bp.route('/order/confirmation')
def order_confirmation():
    """订单确认页面"""
    return render_template('order_confirmation.html')

@main_bp.route('/contact')
def contact():
    """联系我们页面"""
    return render_template('contact.html')

@main_bp.route('/about')
def about():
    """关于我们页面"""
    return render_template('about.html') 