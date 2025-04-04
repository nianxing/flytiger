# 飞虎科技砂纸产品销售平台

这是一个用于代理飞虎科技天鹰砂纸系列产品的在线销售平台。

## 项目概述

本项目提供以下功能：
- 展示天鹰砂纸产品信息和价格
- 在线订单处理
- 客户服务聊天机器人

## 技术架构

- **前端**：HTML, CSS, JavaScript, Bootstrap
- **后端**：Python (Flask)
- **数据存储**：Azure Table Storage 和 Blob Storage
- **订单处理**：Azure Functions
- **客户服务**：Azure Bot Service

## 目录结构

```
flytiger/
├── app/                    # Flask应用主目录
│   ├── static/             # 静态文件 (CSS, JS, 图片)
│   ├── templates/          # HTML模板
│   ├── __init__.py         # Flask应用初始化
│   ├── models.py           # 数据模型
│   ├── routes.py           # 路由定义
│   └── azure_storage.py    # Azure存储操作
├── function_app/           # Azure Functions
│   └── order_processor/    # 订单处理函数
├── bot/                    # Azure Bot Service客户服务机器人
│   ├── app.py              # 机器人应用
│   └── dialogs/            # 对话流程
├── requirements.txt        # 项目依赖
├── config.py               # 配置文件
└── run.py                  # 应用入口点
```

## 部署步骤

### 本地开发环境设置

1. 克隆仓库
```
git clone https://github.com/yourusername/flytiger.git
cd flytiger
```

2. 创建虚拟环境并安装依赖
```
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

3. 设置环境变量
```
set FLASK_APP=run.py
set FLASK_ENV=development
```

4. 运行应用
```
flask run
```

### Azure部署

1. 创建Azure资源:
   - Azure App Service
   - Azure Functions
   - Azure Storage Account
   - Azure Bot Service

2. 配置Azure存储连接字符串

3. 部署Flask应用到Azure App Service

4. 部署订单处理函数到Azure Functions

5. 部署客户服务机器人到Azure Bot Service

## 使用说明

访问网站后，用户可以:
- 浏览产品目录
- 查看产品详情
- 添加商品到购物车
- 提交订单
- 通过聊天机器人获取帮助

## 许可

[许可证信息] 