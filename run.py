from app import create_app
from config import current_config
import os

app = create_app(current_config)

if __name__ == '__main__':
    # 获取 Azure App Service 设置的端口
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port) 