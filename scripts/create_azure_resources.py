#!/usr/bin/env python3
import os
import subprocess
import json
import time
import random
import string

def run_command(command):
    """运行命令并返回输出"""
    print(f"执行: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"错误: {result.stderr}")
        raise Exception(f"命令执行失败: {command}")
    return result.stdout.strip()

def random_string(length=8):
    """生成随机字符串"""
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

def create_resources():
    """创建Azure资源"""
    print("开始创建Azure资源...")
    
    # 配置变量
    resource_group = "flytiger-rg"
    location = "eastasia"  # 可以根据需要更改区域
    app_name_suffix = random_string()
    storage_name = f"flytiger{app_name_suffix}"
    app_service_plan = f"flytiger-plan-{app_name_suffix}"
    web_app_name = f"flytiger-app-{app_name_suffix}"
    function_app_name = f"flytiger-func-{app_name_suffix}"
    bot_app_name = f"flytiger-bot-{app_name_suffix}"
    
    # 登录Azure (如果在本地运行)
    try:
        print("登录Azure...")
        run_command("az login")
    except:
        print("无法登录Azure。如果在CI/CD环境中运行，请确保已配置适当的凭据。")
    
    # 创建资源组
    print(f"创建资源组: {resource_group}")
    try:
        run_command(f"az group create --name {resource_group} --location {location}")
    except:
        print(f"资源组 {resource_group} 可能已存在")
    
    # 创建存储账户
    print(f"创建存储账户: {storage_name}")
    storage_output = run_command(f"az storage account create --name {storage_name} --resource-group {resource_group} --location {location} --sku Standard_LRS")
    storage_info = json.loads(storage_output)
    
    # 获取存储账户连接字符串
    print("获取存储账户连接字符串...")
    connection_string = run_command(f"az storage account show-connection-string --name {storage_name} --resource-group {resource_group} --query connectionString --output tsv")
    
    # 创建App Service计划
    print(f"创建App Service计划: {app_service_plan}")
    run_command(f"az appservice plan create --name {app_service_plan} --resource-group {resource_group} --sku B1")
    
    # 创建Web应用
    print(f"创建Web应用: {web_app_name}")
    run_command(f"az webapp create --name {web_app_name} --resource-group {resource_group} --plan {app_service_plan} --runtime \"PYTHON:3.9\"")
    
    # 创建Function应用
    print(f"创建Function应用: {function_app_name}")
    run_command(f"az functionapp create --name {function_app_name} --resource-group {resource_group} --storage-account {storage_name} --consumption-plan-location {location} --runtime python --runtime-version 3.9 --functions-version 4")
    
    # 创建Bot Web应用
    print(f"创建Bot Web应用: {bot_app_name}")
    run_command(f"az webapp create --name {bot_app_name} --resource-group {resource_group} --plan {app_service_plan} --runtime \"PYTHON:3.9\"")
    
    # 配置应用设置
    print("配置应用设置...")
    run_command(f"az webapp config appsettings set --name {web_app_name} --resource-group {resource_group} --settings FLASK_APP=run.py FLASK_ENV=production AZURE_STORAGE_CONNECTION_STRING=\"{connection_string}\"")
    run_command(f"az functionapp config appsettings set --name {function_app_name} --resource-group {resource_group} --settings AZURE_STORAGE_CONNECTION_STRING=\"{connection_string}\"")
    run_command(f"az webapp config appsettings set --name {bot_app_name} --resource-group {resource_group} --settings AZURE_STORAGE_CONNECTION_STRING=\"{connection_string}\"")
    
    # 创建并设置输出
    output = {
        "resource_group": resource_group,
        "storage_account": storage_name,
        "connection_string": connection_string,
        "app_service_plan": app_service_plan,
        "web_app_name": web_app_name,
        "function_app_name": function_app_name,
        "bot_app_name": bot_app_name,
        "web_app_url": f"https://{web_app_name}.azurewebsites.net",
        "function_app_url": f"https://{function_app_name}.azurewebsites.net",
        "bot_app_url": f"https://{bot_app_name}.azurewebsites.net"
    }
    
    # 保存输出到文件
    with open("azure_resources.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"""
资源创建完成！

Web应用URL: https://{web_app_name}.azurewebsites.net
Function应用URL: https://{function_app_name}.azurewebsites.net
Bot应用URL: https://{bot_app_name}.azurewebsites.net

所有资源信息已保存到 azure_resources.json 文件中。

要在GitHub Actions中使用这些资源，请设置以下secrets:
1. AZURE_CREDENTIALS - 使用 `az ad sp create-for-rbac --name flytiger-deploy --role contributor --scopes /subscriptions/YOUR_SUBSCRIPTION_ID/resourceGroups/{resource_group}` 获取
2. AZURE_STORAGE_CONNECTION_STRING - {connection_string}
3. SECRET_KEY - 生成一个随机字符串作为Flask密钥

接下来，请更新.github/workflows/azure-deploy.yml文件中的应用名称:
- app-name: {web_app_name} (用于Flask应用)
- app-name: {bot_app_name} (用于Bot应用)
- 在Function App部署命令中使用: {function_app_name}
    """)

if __name__ == "__main__":
    create_resources() 