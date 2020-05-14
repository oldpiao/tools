#!/usr/bin/python
#coding=utf-8
'''read结果以字典格式展示,带表名'''
import traceback
import warnings

import MySQLdb

from settings import settings
from setting.sk_log import logger
#warnings.filterwarnings('error', category = MySQLdb.Warning)  
warnings.filterwarnings('ignore', category = MySQLdb.Warning)  

class MySQlDB():
    '''
    conn = db.DB()  --连接数据库
    :param
    host="localhost", user="root",passwd="123456", database="wifijz", charset="utf8"

    conn.read(sql)  --查询数据库，返回结果为二维数组
    :param
    sql SQL语句

    execute(sql,exdata)  --向数据库插入数据，
    :param
    sql为SQL语句（为数据提供占位符）
    exdata为待插入的数据
    '''
        
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
                # print 'sql----------\n',sql
                # print 'exdata----------\n',exdata
                self.n += self.cursor.execute(sql)
                return self.n
                
            except MySQLdb.Warning, e:
                print "MySQLdb.Warning: "  
                print e
                print "----------------------------"

            except MySQLdb.InternalError, e:
                print "MySQLdb.InternalError: "  
                print e
                self.disconnect()
                self.connect()
                continue
                
            except Exception, e:
                print "------------- sk_simple_mysql Exception -------------------------"
                print sql
                print "-----------------------------------------------------------------"
                print exdata
                #print sql % exdata
                traceback.print_exc()
                print e
                return 0
            
        print "------------- sk_simple_mysql Exception -------------------------"
        print sql
        print exdata
        print "run out of max_try_count"
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
            'port': port,
            'charset': charset
        }
        print self.id
        self.connect()
        self.n = 0
       
    def __del__(self):
        self.disconnect()


db = MySQlDB(**settings['MySQL'])