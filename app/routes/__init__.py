from app.routes.main import main_bp
from app.routes.products import products_bp
from app.routes.orders import orders_bp
from app.routes.cart import cart_bp

# Export blueprints
__all__ = ['main_bp', 'products_bp', 'orders_bp', 'cart_bp'] 