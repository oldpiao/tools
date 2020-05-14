#!/usr/bin/python
#coding=utf-8

import traceback
import warnings

import MySQLdb

from settings import settings

#warnings.filterwarnings('error', category = MySQLdb.Warning)  
warnings.filterwarnings('ignore', category = MySQLdb.Warning)  

class DB():
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
    def set_id(self, host,user,passwd,database,charset):
        self.id=(host,user,passwd,database,charset)
    
        
    def connect(self):
        self.db = MySQLdb.connect(self.id[0],self.id[1],self.id[2],self.id[3],charset=self.id[4])
        self.cursor = self.db.cursor()
        
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
        self.cursor.execute(sql)
        return self.cursor.fetchall()
        
    def write(self, sql, exdata):
        self.n=0
        if isinstance(exdata, (tuple, list)):
            for dic in exdata:
                self.execute(sql, dic)
        else:
            self.execute(sql, exdata)
        self.db.commit()
        return self.n
            
    def __init__(self, host, user,passwd,database, charset="utf8"):
        self.db = None
        self.cursor = None
        self.set_id(host=host,user=user,passwd=passwd,database=database,charset=charset)
        self.connect()
        self.n = 0
       
    def __del__(self):
        self.disconnect()


db = DB(**settings['MySQL'])