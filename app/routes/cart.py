from flask import Blueprint, render_template

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

@cart_bp.route('/')
def index():
    return render_template('cart/index.html', title='购物车')

@cart_bp.route('/checkout')
def checkout():
    return render_template('cart/checkout.html', title='结算') 