from flask import Blueprint, render_template, request, redirect, url_for, flash

# Create cart blueprint
cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

# Example cart items - in a real app, this would be stored in session or database
CART_ITEMS = [
    {'product': {
        'id': 1,
        'name': '天鹰砂纸-P80',
        'description': '适用于木材粗磨、金属表面除锈',
        'specifications': '230mm x 280mm',
        'price': 8.5,
        'image': 'eagle_p80.jpg'
    }, 'quantity': 2},
    {'product': {
        'id': 3,
        'name': '天鹰砂纸-P180',
        'description': '适用于木材细磨、涂层磨平',
        'specifications': '230mm x 280mm',
        'price': 7.5,
        'image': 'eagle_p180.jpg'
    }, 'quantity': 1}
]

@cart_bp.route('/')
def index():
    """Shopping cart page"""
    total = sum(item['product']['price'] * item['quantity'] for item in CART_ITEMS)
    return render_template('cart/index.html', cart_items=CART_ITEMS, total=total)

@cart_bp.route('/add', methods=['POST'])
def add():
    """Add item to cart"""
    # In a real app, would add product to session or database
    product_id = int(request.form.get('product_id'))
    quantity = int(request.form.get('quantity', 1))
    
    flash(f'已添加商品到购物车！')
    return redirect(url_for('cart.index'))

@cart_bp.route('/checkout')
def checkout():
    """Redirect to checkout page"""
    return redirect(url_for('orders.checkout')) 