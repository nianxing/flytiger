"""Gunicorn config file"""

# 绑定IP和端口
bind = "0.0.0.0:8000"

# 工作进程数
workers = 4

# 超时时间
timeout = 120

# 访问日志格式
accesslog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# 错误日志配置
errorlog = "-"
loglevel = "info"

# 预加载应用
preload_app = True

# 工作模式
worker_class = "sync" 