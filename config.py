import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    """基本配置"""
    # Flask配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    DEBUG = False
    
    # Azure存储配置
    AZURE_STORAGE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
    AZURE_TABLE_NAME = os.environ.get('AZURE_TABLE_NAME') or 'orders'
    AZURE_BLOB_CONTAINER = os.environ.get('AZURE_BLOB_CONTAINER') or 'productimages'
    
    # 应用配置
    COMPANY_NAME = '飞虎科技'
    PRODUCT_LINE = '天鹰砂纸'
    
class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    
class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False

# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# 当前配置
current_config = config[os.environ.get('FLASK_ENV') or 'default'] 