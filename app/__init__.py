from flask import Flask, render_template, request, g
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
    
    # 语言偏好处理
    @app.before_request
    def get_user_language():
        # 优先从Cookie中获取语言设置
        lang = request.cookies.get('user_lang')
        
        # 如果Cookie中没有设置，再看URL参数
        if not lang:
            lang = request.args.get('lang')
            
        # 如果都没有，则使用默认值cn
        if not lang:
            lang = 'cn'
            
        # 只允许支持的语言
        if lang not in ['cn', 'en']:
            lang = 'cn'
            
        # 将语言设置保存在g对象中，方便所有路由函数访问
        g.lang = lang
    
    # 添加语言模板全局变量
    @app.context_processor
    def inject_language():
        # 从g对象中获取语言设置
        lang = getattr(g, 'lang', 'cn')
        return {'lang': lang}
    
    # 注册错误处理器
    register_error_handlers(app)
    
    return app

def register_error_handlers(app):
    """注册错误处理器"""
    @app.errorhandler(404)
    def page_not_found(e):
        # 从g对象获取语言设置
        lang = getattr(g, 'lang', 'cn')
        return render_template('errors/404.html', lang=lang), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        # 从g对象获取语言设置
        lang = getattr(g, 'lang', 'cn')
        return render_template('errors/500.html', lang=lang), 500

# 导入Flask的render_template函数
from flask import render_template 