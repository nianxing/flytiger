from flask import Flask, render_template
import os

def create_app(config_object):
    """创建并配置Flask应用"""
    app = Flask(__name__)
    app.config.from_object(config_object)
    
    # 注册蓝图
    from app.routes.main import main_bp
    from app.routes.products import products_bp
    from app.routes.orders import orders_bp
    from app.routes.cart import cart_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(cart_bp)
    
    # 注册错误处理器
    register_error_handlers(app)
    
    return app

def register_error_handlers(app):
    """注册错误处理器"""
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

# 导入Flask的render_template函数
from flask import render_template 