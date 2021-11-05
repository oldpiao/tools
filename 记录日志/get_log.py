import os
import logging
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler


def makedirs(f_path):
    f_dir, f_name = os.path.split(f_path)
    if not os.path.isdir(f_dir):
        os.makedirs(f_dir)


class Logger(object):
    def __init__(self, level, name=None):
        """
        args:
            level: 日志级别
            name: 日志名，可以是任意名，如果是单独存的日志尽量起一个名字，否则可能会和别的日志的设置合并
        """
        # 日志输出格式
        self.formatter = logging.Formatter('[%(asctime)s] - %(filename)s] - %(levelname)s: %(message)s')
        self.logger = logging.getLogger(name=name)
        self.logger.setLevel(level)

    def to_console(self):
        """设置日志打印到控制台"""
        ch = logging.StreamHandler()
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)
        return self

    def to_file(self, filename):
        """设置日志保存日志到日志文件"""
        makedirs(filename)
        hdlr = logging.FileHandler(filename, 'a', encoding='utf-8')
        hdlr.setFormatter(self.formatter)
        self.logger.addHandler(hdlr)
        return self

    def to_file_rotating(self, filename, maxBytes=50*1024*1024, *args, **kwargs):
        """设置日志保存日志到日志文件，按文件大小切分日志"""
        makedirs(filename)
        hdlr = RotatingFileHandler(filename, maxBytes=maxBytes, *args, **kwargs)
        hdlr.setFormatter(self.formatter)
        self.logger.addHandler(hdlr)
        return self

    def to_file_timed_rotating(self, filename, when="midnight", interval=1, backupCount=7, *args, **kwargs):
        """设置日志保存日志到日志文件，按时间切分日志"""
        makedirs(filename)
        hdlr = TimedRotatingFileHandler(filename, when=when, interval=interval,
                                        backupCount=backupCount, *args, **kwargs)
        hdlr.setFormatter(self.formatter)
        self.logger.addHandler(hdlr)
        return self

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)
