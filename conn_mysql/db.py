#!/usr/bin/python
# coding=utf-8

import traceback
import warnings

import pymysql


# warnings.filterwarnings('error', category = MySQLdb.Warning)
warnings.filterwarnings('ignore', category=pymysql.Warning)


class MysqlConn(object):
    def __init__(self, host, user, password, db, port=3306, charset="utf8"):
        self.db = None
        self.cursor = None
        self.info = dict(host=host, port=port, user=user, password=password, db=db, charset=charset)
        self.connect()
        self.n = 0

    def connect(self):
        self.db = pymysql.connect(
            cursorclass=pymysql.cursors.DictCursor,
            **self.info,
        )
        self.cursor = self.db.cursor()

    def disconnect(self):
        if self.db is not None:
            self.db.commit()
            if self.cursor is not None:
                self.cursor.close()
            self.db.close()
        self.db = None
        self.cursor = None

    def execute(self, sql, exdata, max_try_count=3):
        while max_try_count > 0:
            max_try_count -= 1
            try:
                sql = sql % exdata
                # print 'sql----------\n',sql
                # print 'exdata----------\n',exdata
                self.n += self.cursor.execute(sql)
                return self.n

            except pymysql.Warning as e:
                print("MySQLdb.Warning: ")
                print(e)
                print("----------------------------")

            except pymysql.InternalError as e:
                print("MySQLdb.InternalError: ")
                print(e)
                self.disconnect()
                self.connect()
                continue

            except Exception as e:
                print("------------- sk_simple_mysql Exception -------------------------")
                print(sql)
                print("-----------------------------------------------------------------")
                print(exdata)
                # print sql % exdata
                traceback.print_exc()
                print(e)
                return 0

        print("------------- sk_simple_mysql Exception -------------------------")
        print(sql)
        print(exdata)
        print("run out of max_try_count")
        return 0

    def read(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def read_many(self, sql, size):
        '''一次读取size条数据'''
        self.cursor.execute(sql)
        while True:
            data = self.cursor.fetchmany(size)
            if data:
                yield data
            else:
                break

    def write(self, sql, exdata):
        self.n = 0
        if isinstance(exdata, (tuple, list)):
            for dic in exdata:
                self.execute(sql, dic)
        else:
            self.execute(sql, exdata)
        self.db.commit()
        return self.n

    def __del__(self):
        self.disconnect()


if __name__ == '__main__':
    conn = MysqlConn('127.0.0.1', 'root', 'bjm22122', 'audit')
    sql = "select * from audit_info;"
    print(conn.read(sql))
