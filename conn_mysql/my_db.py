# -*- coding:utf-8 -*-

# import db
# import json
#
# db.create_db_manager('localhost',3306,'zkwh_es','root','zkwh56jm')
# a = db.DB()
# print a.selectall('es_labels')


import db2

def db():
    return db2.Connection(host='localhost', database='zkwh_es', user='root', password='zkwh56jm')
db = db()
# db.execute("insert into `picdownload` (`hash`) values(%s)",hash)  # 插入
print db.query("select * from es_labels")  # 查询