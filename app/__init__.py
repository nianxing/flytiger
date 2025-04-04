from flask import Flask

def create_app(config_object):
    """创建并配置Flask应用"""
    app = Flask(__name__)
    app.config.from_object(config_object)
    
    # 注册蓝图
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    # 注册错误处理
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