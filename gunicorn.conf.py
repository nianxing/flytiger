"""Gunicorn config file"""
import os

# Bind to the port provided by Azure
bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"

# Worker configuration
workers = 4
worker_class = "sync"
timeout = 120

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Application module
wsgi_app = "application:app"

# 访问日志格式
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# 预加载应用
preload_app = True 