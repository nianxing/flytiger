from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')

@orders_bp.route('/')
def index():
    return render_template('orders/index.html', title='订单列表')

@orders_bp.route('/<order_id>')
def detail(order_id):
    return render_template('orders/detail.html', title='订单详情', order_id=order_id)

@orders_bp.route('/checkout')
def checkout():
    """Checkout page"""
    return render_template('orders/checkout.html')

@orders_bp.route('/process', methods=['POST'])
def process():
    """Process order submission"""
    # In a real app, we would save the order to a database or Azure Table
    # For now, just simulate success
    flash('订单已成功提交！')
    return redirect(url_for('orders.confirmation'))

@orders_bp.route('/confirmation')
def confirmation():
    """Order confirmation page"""
    # In a real app, would display order details from database
    return render_template('orders/confirmation.html', now=datetime.now) 