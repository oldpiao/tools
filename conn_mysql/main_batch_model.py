# -*- coding:utf-8 -*-
import sys
import json

import es_lib
from es_lib import csvtoes
from es_lib import mysqltoes
from es_lib import jsontoes
from es_lib import exceltoes
from setting.sk_log import logger

def key_value(key,param):
    '''获取普通格式的参数,
    参数格式: python xxx.py key value'''
    if key in param:
        value = param[param.index(key) + 1]
        logger.info(key+':'+value)
        return value
    else:
        exit(help.__doc__)

def _get_json(dir):
    '''打开json文件'''
    with open(dir, 'r') as f:
        data = f.read()
    return json.dumps(data)

def key_json(key,param):
    '''获取json格式的参数'''
    if key in param:
        value = param[param.index(key) + 1]
        logger.info(key+':'+value)
        try:  # 传递json
            return json.loads(value)
        except:  # 传递json文件地址
            return _get_json(value)

def batch_key_value(key,deal_with_some, sometoes):
    if '-%stask'%key in param:
        my_id = int(key_value('-%stask'%key, param))
        print deal_with_some(father_id=my_id)
        exit()
    if '-%sstateall' % key in param:
        my_id = int(key_value('-%sstateall' % key, param))
        print sometoes.state_it_all(my_id)
        exit()
    if '-%sstateone'%key in param:
        my_id = int(key_value('-%sstateone'%key, param))
        print sometoes.state_it_one(my_id)
        exit()
    if '-%sretryall' % key in param:
        my_id = int(key_value('-%sretryall' % key, param))
        print sometoes.state_it_all(my_id)
        exit()
    if '-%sretryone'%key in param:
        my_id = int(key_value('-%sretryone'%key, param))
        print sometoes.state_it_one(my_id)
        exit()
    if '-%sdeleteall' % key in param:
        my_id = int(key_value('-%sdeleteall' % key, param))
        print sometoes.deleteall(my_id)
        exit()
    if '-%sdeleteone'%key in param:
        my_id = int(key_value('-%sdeleteone'%key, param))
        print sometoes.deleteone(my_id)
        exit()
    if '-%sinfo'%key in param:
        param_json = key_json('-%sinfo'%key, param)
        print json.dumps(sometoes.get_info(param_json))
        exit()


def help():
    '''
    -{key}info json/jsondir:  获取{key}数据前五行数据
    -{key}task id:            创建{key}中导入子任务并开始执行,参数为父任务id
    -{key}stateall id:        开始{key}数据导入父任务
    -{key}stateone id:        开始{key}数据导入子任务
    -{key}retryall id:        重试{key}数据导入父任务
    -{key}retryone id:        重试{key}数据导入子任务
    -{key}deleteall id:       删除{key}数据导入父任务
    -{key}deleteone id:       删除{key}数据导入子任务
    '''
    a = ['csv','mysql','json','excel']
    my_help = '''es项目帮助文档:
    -[h/H/help]:              帮助'''
    for i in a:
        my_help+=help.__doc__.format(key=i)
        if i=='excel':
            my_help+='-excelsheet dir:          获取excel的分页信息'
    return my_help

def main(param):
    a = [
        ['csv',es_lib.deal_with_csv,csvtoes],
        ['mysql',es_lib.deal_with_mysql,mysqltoes],
        ['json',es_lib.deal_with_json,jsontoes],
        ['excel',es_lib.deal_with_excel,exceltoes]
    ]
    if '-h' in param or '-H' in param or 'help' in param:
        print help()
        exit()
    if '-excelsheet' in param:
        param_json = key_value('-excelsheet', param)
        print json.dumps(exceltoes.get_sheet(param_json))
        exit()
    for i in a:
        batch_key_value(*i)


if __name__ == '__main__':
    param = sys.argv
    # print param
    logger.info('main params:'+str(param[1:]))
    main(param[1:])

