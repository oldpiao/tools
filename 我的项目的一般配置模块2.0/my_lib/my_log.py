# encoding=utf-8
import logging
import time
# log_path是存放日志的路径
import os


cur_path = os.path.dirname(os.path.realpath(__file__))
default_log_path = os.path.join(os.path.dirname(cur_path), 'logs')


class Log(object):

    def __init__(self, level='debug', log_path=default_log_path):
        # 如果不存在这个logs文件夹，就自动创建一个
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        self.log_path = log_path
        # 文件的命名
        level = level.lower()
        self.levels = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "warn": logging.WARN,
            "error": logging.ERROR,
            "critical": logging.CRITICAL,
        }
        self.level = self.levels[level]
        # 不会随时间改变
        # self.logname = os.path.join(self.log_path, '%s.log' % time.strftime('%Y_%m_%d'))
        self.logger = logging.getLogger()
        self.logger.setLevel(self.level)
        # 日志输出格式
        self.formatter = logging.Formatter('[%(asctime)s] - %(filename)s] - %(levelname)s: %(message)s')

    @property
    def logname(self):
        # 会随时间改变
        return os.path.join(self.log_path, '%s.log' % time.strftime('%Y_%m_%d'))

    def __console(self, level, message):
        # 创建一个FileHandler，用于写到本地
        fh = logging.FileHandler(self.logname, 'a', encoding='utf-8')  # 这个是python3的
        fh.setLevel(self.level)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        # 创建一个StreamHandler,用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(self.level)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        # 这两行代码是为了避免日志输出重复问题
        self.logger.removeHandler(ch)
        self.logger.removeHandler(fh)
        # 关闭打开的文件
        fh.close()

    def debug(self, message):
        self.__console('debug', message)

    def info(self, message):
        self.__console('info', message)

    def warning(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)
