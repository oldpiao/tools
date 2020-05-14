#!/usr/bin/python
#coding=utf-8

import traceback
import warnings

import MySQLdb

from settings import settings
from setting.sk_log import logger
#warnings.filterwarnings('error', category = MySQLdb.Warning)  
warnings.filterwarnings('ignore', category = MySQLdb.Warning)  

class MyDB():
        
    def connect(self):
        self.db = MySQLdb.connect(**self.id)
        self.cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)  # 将结果以dict格式展示
        
    def disconnect(self):
        if self.db is not None:
            self.db.commit()
            if self.cursor is not None:
                self.cursor.close()
            self.db.close()
        self.db=None
        self.cursor=None
        
    def execute(self, sql, exdata, max_try_count=3):
        
        while max_try_count > 0:
            max_try_count-=1
            try:
                sql = sql % exdata
                # logger.info('sql----------\n',sql)
                # logger.info('exdata----------\n',exdata)
                self.n += self.cursor.execute(sql)
                return self.n
                
            except MySQLdb.Warning, e:
                logger.info("MySQLdb.Warning: ")
                logger.info(e)
                logger.info("----------------------------")

            except MySQLdb.InternalError, e:
                logger.info("MySQLdb.InternalError: ")
                logger.info(e)
                self.disconnect()
                self.connect()
                continue
                
            except Exception, e:
                logger.info("------------- sk_simple_mysql Exception -------------------------")
                logger.info(sql)
                logger.info("-----------------------------------------------------------------")
                logger.info(exdata)
                #logger.info(sql % exdata)
                traceback.print_exc()
                logger.info(e)
                return 0
            
        logger.info("------------- sk_simple_mysql Exception -------------------------")
        logger.info(sql)
        logger.info(exdata)
        logger.info("run out of max_try_count")
        return 0
        
    def read(self, sql):
        '''一次读取全部数据'''
        logger.info(sql)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def read_many(self, sql, size):
        '''一次读取size条数据'''
        logger.info(sql)
        self.cursor.execute(sql)
        while True:
            data = self.cursor.fetchmany(size)
            if data:
                yield data
            else:
                break

    def read_one(self, sql):
        '''一次读取1条数据'''
        logger.info(sql)
        self.cursor.execute(sql)
        while True:
            data = self.cursor.fetchone()
            if data:
                yield data
            else:
                break

    def read_count(self, sql):
        '''统计一次查询的数据量'''
        logger.info(sql)
        self.cursor.execute(sql)
        return self.cursor.rowcount

    def write(self, sql, exdata):
        self.n=0
        logger.info(sql)
        logger.info(exdata)
        if isinstance(exdata, (tuple, list)):
            for dic in exdata:
                self.execute(sql, dic)
        else:
            self.execute(sql, exdata)
        self.db.commit()
        return self.n
            
    def __init__(self, user, passwd, db, host, port=3306, charset="utf8",*args,**kwargs):
        self.db = None
        self.cursor = None
        self.id = {
            'user': user,
            'passwd': passwd,
            'db': db,
            'host': host,
            'port': int(port),
            'charset': charset
        }
        self.connect()
        self.n = 0
       
    def __del__(self):
        self.disconnect()


db = MyDB(**settings['MySQL'])