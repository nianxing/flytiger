#!/bin/bash

# 打印Python版本
echo "Python version:"
python --version

# 安装依赖项
echo "Installing dependencies..."
pip install -r requirements.txt

# 启动应用
echo "Starting application..."
gunicorn --bind=0.0.0.0:8000 run:app --config gunicorn.conf.py 