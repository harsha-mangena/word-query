command = '.venv/bin/gunicorn'
bind = '0.0.0.0:7979'
workers = 17
errorlog = 'logs/gunicorn_error.log'
accesslog = 'logs/gunicorn_access.log'
loglevel = 'info'
