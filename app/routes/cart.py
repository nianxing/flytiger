from flask import Blueprint, render_template, request, redirect, url_for, session, flash, g

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
    """购物车页面"""
    lang = g.lang
    cart_items = session.get('cart', [])
    
    # 计算总价
    total_price = sum(item.get('price', 0) * item.get('quantity', 0) for item in cart_items)
    
    return render_template('cart/index.html', cart_items=cart_items, total_price=total_price)

@cart_bp.route('/add', methods=['POST'])
def add():
    """添加商品到购物车"""
    lang = g.lang
    product_id = int(request.form.get('product_id'))
    quantity = int(request.form.get('quantity', 1))
    
    # 从产品列表中获取产品信息
    from app.routes.products import PRODUCTS
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    
    if not product:
        flash('产品不存在' if lang == 'cn' else 'Product does not exist', 'danger')
        return redirect(url_for('products.index'))
    
    # 获取当前购物车
    cart = session.get('cart', [])
    
    # 检查商品是否已经在购物车中
    cart_item = next((item for item in cart if item['id'] == product_id), None)
    
    # 处理产品的多语言名称和描述
    name = product['name'][lang] if isinstance(product['name'], dict) else product['name']
    description = product['description'][lang] if isinstance(product['description'], dict) else product['description']
    
    if cart_item:
        # 如果已在购物车中，更新数量
        cart_item['quantity'] += quantity
        flash('已更新购物车' if lang == 'cn' else 'Cart updated successfully', 'success')
    else:
        # 如果不在购物车中，添加新商品
        cart.append({
            'id': product_id,
            'name': name,
            'description': description,
            'price': product['price'],
            'image': product['image'],
            'quantity': quantity
        })
        flash('已添加到购物车' if lang == 'cn' else 'Added to cart successfully', 'success')
    
    # 更新session中的购物车
    session['cart'] = cart
    
    return redirect(url_for('cart.index'))

@cart_bp.route('/update', methods=['POST'])
def update():
    """更新购物车中的商品数量"""
    lang = g.lang
    product_id = int(request.form.get('product_id'))
    quantity = int(request.form.get('quantity', 1))
    
    cart = session.get('cart', [])
    
    # 查找要更新的商品
    cart_item = next((item for item in cart if item['id'] == product_id), None)
    
    if cart_item:
        if quantity > 0:
            # 更新数量
            cart_item['quantity'] = quantity
            flash('购物车已更新' if lang == 'cn' else 'Cart updated successfully', 'success')
        else:
            # 如果数量为0，从购物车中移除
            cart.remove(cart_item)
            flash('商品已从购物车中移除' if lang == 'cn' else 'Item removed from cart', 'success')
    
    session['cart'] = cart
    
    return redirect(url_for('cart.index'))

@cart_bp.route('/remove/<int:product_id>')
def remove(product_id):
    """从购物车中移除商品"""
    lang = g.lang
    cart = session.get('cart', [])
    
    # 查找要移除的商品
    cart_item = next((item for item in cart if item['id'] == product_id), None)
    
    if cart_item:
        cart.remove(cart_item)
        session['cart'] = cart
        flash('商品已从购物车中移除' if lang == 'cn' else 'Item removed from cart', 'success')
    
    return redirect(url_for('cart.index'))

@cart_bp.route('/clear')
def clear():
    """清空购物车"""
    lang = g.lang
    session['cart'] = []
    flash('购物车已清空' if lang == 'cn' else 'Cart cleared successfully', 'success')
    
    return redirect(url_for('cart.index'))

@cart_bp.route('/checkout')
def checkout():
    """Redirect to checkout page"""
    return redirect(url_for('orders.checkout')) 