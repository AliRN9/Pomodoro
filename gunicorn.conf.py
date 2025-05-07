import os

from uvicorn_worker import UvicornWorker
from dotenv import load_dotenv

bind = '0.0.0.0:8000'
# default_workers = multiprocessing.cpu_count() * 2 + 1
worker_class = UvicornWorker
workers = 4

errorlog = '-'
loglevel = 'info'
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

environment = os.getenv('ENVIRONMENT')
env = os.path.join(os.getcwd(), f'.{environment}.env')
if os.path.exists(env):
    print(f"{env=}")
    load_dotenv(dotenv_path=env, override=True)
