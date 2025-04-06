from flask import Blueprint, render_template

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')

@orders_bp.route('/')
def index():
    return render_template('orders/index.html', title='订单列表')

@orders_bp.route('/<order_id>')
def detail(order_id):
    return render_template('orders/detail.html', title='订单详情', order_id=order_id) 