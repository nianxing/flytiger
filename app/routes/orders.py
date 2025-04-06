from flask import Blueprint, render_template, request, redirect, url_for, session, flash, g
from datetime import datetime

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')

@orders_bp.route('/')
def index():
    lang = g.lang
    title = 'Order List' if lang == 'en' else '订单列表'
    return render_template('orders/index.html', title=title)

@orders_bp.route('/<order_id>')
def detail(order_id):
    lang = g.lang
    title = 'Order Details' if lang == 'en' else '订单详情'
    return render_template('orders/detail.html', title=title, order_id=order_id)

@orders_bp.route('/checkout')
def checkout():
    """结算页面"""
    lang = g.lang
    cart_items = session.get('cart', [])
    
    if not cart_items:
        flash('购物车为空，请先添加商品' if lang == 'cn' else 'Your cart is empty. Please add items first.', 'warning')
        return redirect(url_for('products.index'))
    
    # 计算总价
    total_price = sum(item.get('price', 0) * item.get('quantity', 0) for item in cart_items)
    
    return render_template('orders/checkout.html', cart_items=cart_items, total_price=total_price)

@orders_bp.route('/place_order', methods=['POST'])
def place_order():
    """提交订单"""
    lang = g.lang
    
    # 获取表单数据
    name = request.form.get('name')
    phone = request.form.get('phone')
    address = request.form.get('address')
    payment_method = request.form.get('payment_method')
    
    # 获取购物车
    cart_items = session.get('cart', [])
    
    if not cart_items:
        flash('购物车为空，请先添加商品' if lang == 'cn' else 'Your cart is empty. Please add items first.', 'warning')
        return redirect(url_for('products.index'))
    
    # 这里应该将订单信息存入数据库
    # 现在只是模拟成功提交
    
    # 生成订单号
    import random
    order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
    
    # 清空购物车
    session['cart'] = []
    
    # 存储订单信息到session，以便确认页面使用
    session['order'] = {
        'order_number': order_number,
        'name': name,
        'phone': phone,
        'address': address,
        'payment_method': payment_method,
        'items': cart_items,
        'total_price': sum(item.get('price', 0) * item.get('quantity', 0) for item in cart_items),
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    flash('订单已成功提交' if lang == 'cn' else 'Order submitted successfully', 'success')
    return redirect(url_for('orders.confirmation'))

@orders_bp.route('/confirmation')
def confirmation():
    """订单确认页面"""
    lang = g.lang
    order = session.get('order', None)
    
    if not order:
        flash('没有找到订单信息' if lang == 'cn' else 'No order information found', 'danger')
        return redirect(url_for('main.index'))
    
    return render_template('orders/confirmation.html', order=order) 