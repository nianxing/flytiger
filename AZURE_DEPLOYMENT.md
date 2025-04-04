# Azure 部署指南

本指南说明如何将飞虎科技天鹰砂纸销售网站部署到Azure云平台。

## 自动部署方法

我们提供了两种部署方式：
1. 使用Python脚本自动创建资源并本地部署
2. 使用GitHub Actions进行持续集成和部署(CI/CD)

## 先决条件

- 安装 [Azure CLI](https://docs.microsoft.com/zh-cn/cli/azure/install-azure-cli)
- 安装 [Python 3.9](https://www.python.org/downloads/) 或更高版本
- 拥有Azure订阅

## 选项1：使用Python脚本部署

### 步骤1：登录Azure

```bash
az login
```

### 步骤2：创建Azure资源

运行我们提供的脚本来自动创建所有需要的Azure资源：

```bash
python scripts/create_azure_resources.py
```

此脚本将创建：
- 资源组
- 存储账户(用于表存储和Blob存储)
- App Service计划
- Flask Web应用
- Function应用
- Bot Web应用

脚本执行完成后，将生成`azure_resources.json`文件，其中包含所有创建的资源信息。

### 步骤3：部署应用

使用Azure CLI部署应用：

```bash
# 部署Flask应用
az webapp deploy --resource-group <资源组名称> --name <Web应用名称> --src-path . --type zip

# 部署Function应用
cd function_app
func azure functionapp publish <Function应用名称>
cd ..

# 部署Bot应用
cd bot
zip -r ../bot.zip .
cd ..
az webapp deploy --resource-group <资源组名称> --name <Bot应用名称> --src-path bot.zip --type zip
```

### 步骤4：上传产品图片

设置存储连接字符串环境变量并运行上传脚本：

```bash
export AZURE_STORAGE_CONNECTION_STRING="<存储连接字符串>"
python scripts/upload_images.py
```

## 选项2：使用GitHub Actions进行CI/CD

### 步骤1：创建服务主体

使用以下命令创建一个具有资源组贡献者权限的服务主体：

```bash
az ad sp create-for-rbac --name flytiger-deploy --role contributor \
                          --scopes /subscriptions/<订阅ID>/resourceGroups/<资源组名称> \
                          --sdk-auth
```

命令会输出一个JSON对象，包含身份验证信息。

### 步骤2：配置GitHub仓库密钥

在GitHub仓库中，添加以下机密：

1. `AZURE_CREDENTIALS` - 设置为上一步输出的整个JSON对象
2. `AZURE_STORAGE_CONNECTION_STRING` - 设置为Azure存储连接字符串
3. `SECRET_KEY` - 设置为一个随机字符串作为Flask密钥

### 步骤3：将代码推送到GitHub

将代码推送到GitHub仓库，工作流将自动运行：

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

## 访问已部署的应用

部署完成后，可以通过以下URL访问应用：

- Web应用：`https://<web_app_name>.azurewebsites.net`
- Function应用：`https://<function_app_name>.azurewebsites.net`
- Bot应用：`https://<bot_app_name>.azurewebsites.net`

## 故障排除

如果遇到问题，请检查：

1. Azure资源是否已正确创建
2. 应用设置中是否包含正确的环境变量
3. GitHub Actions工作流日志中是否有错误信息

更多信息，请参考[Azure Web应用文档](https://docs.microsoft.com/zh-cn/azure/app-service/)和[Azure Functions文档](https://docs.microsoft.com/zh-cn/azure/azure-functions/)。 