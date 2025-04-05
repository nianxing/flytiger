# 飞虎科技天鹰砂纸销售平台

这是一个专业代理销售天鹰砂纸系列产品的在线平台，基于Python Flask开发，并部署在Azure云服务上。

## 项目功能

- 产品展示和详情页
- 产品分类和筛选
- 购物车功能
- 在线订单处理
- 客户服务聊天机器人

## 技术架构

- **前端**: HTML, CSS, JavaScript, Bootstrap 5
- **后端**: Python Flask
- **数据存储**: Azure Storage (Table & Blob)
- **云服务**: 
  - Azure App Service (Web应用)
  - Azure Functions (订单处理)
  - Azure Bot Service (客户服务)

## 本地开发

### 环境要求

- Python 3.9+
- pip 包管理器

### 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/yourusername/flytiger.git
cd flytiger
```

2. 创建并激活虚拟环境
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置环境变量
```bash
# Windows
set FLASK_APP=run.py
set FLASK_ENV=development
# Linux/Mac
export FLASK_APP=run.py
export FLASK_ENV=development
```

5. 运行开发服务器
```bash
flask run
```

应用将在 http://127.0.0.1:5000/ 上运行。

## Azure部署指南

### 自动部署（GitHub Actions）

1. **创建Azure资源**

   - 创建资源组
   - 创建Web应用（Python 3.9）
   - 创建存储账户

2. **配置GitHub Secrets**

   在GitHub仓库设置中，添加以下secrets：
   - `AZURE_CREDENTIALS`: Azure服务主体凭证（JSON格式）
   - `SECRET_KEY`: Flask应用密钥
   - `AZURE_STORAGE_CONNECTION_STRING`: Azure存储账户连接字符串

3. **推送代码**

   GitHub Actions会自动部署代码到Azure。工作流配置见`.github/workflows/azure-deploy.yml`。

### 手动部署

1. **准备部署包**
```bash
zip -r deployment.zip . -x "venv/*" -x ".git/*"
```

2. **在Azure Portal部署**
   - 进入Web应用 > 部署中心
   - 选择"手动部署" > 上传ZIP文件
   - 上传deployment.zip

3. **配置应用设置**
   - 进入Web应用 > 配置 > 应用设置
   - 添加必要的环境变量

## 项目目录结构

```
flytiger/
├── app/                    # Flask应用
│   ├── static/             # 静态文件
│   ├── templates/          # HTML模板
│   ├── __init__.py         # 应用初始化
│   ├── models.py           # 数据模型
│   ├── routes.py           # 路由定义
│   └── azure_storage.py    # Azure存储操作
├── function_app/           # Azure Functions
├── bot/                    # 聊天机器人
├── requirements.txt        # 项目依赖
├── run.py                  # 应用入口
├── config.py               # 配置文件
├── startup.sh              # Azure启动脚本
├── gunicorn.conf.py        # Gunicorn配置
└── .github/workflows/      # GitHub Actions配置
```

## 常见问题排查

1. **应用无法启动**
   - 检查启动日志：Azure Portal > Web应用 > 日志流
   - 确认启动命令正确：`sh startup.sh`

2. **Azure存储连接问题**
   - 验证连接字符串是否正确
   - 检查存储账户中是否已创建orders表和productimages容器

3. **部署失败**
   - 查看GitHub Actions运行日志
   - 确认Azure凭证配置正确

## 贡献指南

1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交修改 (`git commit -m 'Add amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 许可证

[MIT](LICENSE) 