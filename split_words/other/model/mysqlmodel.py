from split_words.settings import MYSQL_INFO
from split_words.my_lib.db import MysqlConn
from split_words.settings import logger

__all__ = ['AuditInfo']


class AuditInfo(object):

    def __init__(self):
        self.conn = MysqlConn(**MYSQL_INFO)
        self.table = 'audit_info'

    def select_not_split(self):
        sql = 'SELECT * FROM %s where question_words is NULL;' % self.table
        logger.info(sql)
        return self.conn.read(sql)
