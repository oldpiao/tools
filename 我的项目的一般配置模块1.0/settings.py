import os
from .my_lib.my_log import Log

ROOT_DIR_P = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # 项目根目录
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # 模块根目录
cur_dir = os.path.dirname(os.path.abspath(__file__)) or os.getcwd()

logger = Log()
# logger = Logger(logname=os.path.join(ROOT_DIR, 'log.txt'), loglevel=1, logger="fox").getlog()
# logger = Logger2(loglevel=1, logger="fox").getlog()
