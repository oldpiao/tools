# -*- coding:utf-8 -*-
'''
一个python2的系统命令调用python程序的模板
oldpiao
'''

import sys
import json

from setting.sk_log import logger

def key_value(key, param):
    '''获取普通格式的参数,
    参数格式: python xxx.py key value'''
    if key in param:
        value = param[param.index(key) + 1]
        logger.info(key + ':' + value)
        return value
    else:
        exit(help.__doc__)

def _get_json(dir):
    '''打开json文件'''
    with open(dir, 'r') as f:
        data = f.read()
    return json.dumps(data)

def key_json(key, param):
    '''获取json格式的参数'''
    if key in param:
        value = param[param.index(key) + 1]
        logger.info(key + ':' + value)
        try:  # 传递json
            return json.loads(value)
        except:  # 传递json文件地址
            return _get_json(value)

def help():
    '''
    -[h/H/help]:        帮助
    -a id:              XXXXX
    -b json/json_dir:   XXXXX
    -c str:             XXXXX
    -d str:             result: json XXXXX

    '''
    return help.__doc__


def main(param):
    if '-h' in param or '-H' in param or 'help' in param:
        print help.__doc__
        exit()

    if '-a' in param:
        my_id = int(key_value('-a', param))
        print '传参为int型的:%d'%my_id
        exit()
    if '-b' in param:
        param_json = key_json('-b', param)
        print '传参为json格式或json文件路径的:%s'%str(param_json)
        exit()
    if '-c' in param:
        param_json = key_value('-c', param)
        print '传参为字符串的:%s'%param_json
        exit()
    if '-d' in param:
        param_json = key_value('-d', param)
        print '返回结果期待为json的:%s'%json.dumps({'param': param_json})
        exit()
    else:
        print help.__doc__
        exit()


if __name__ == '__main__':
    param = sys.argv
    # print param
    logger.info('main params:' + str(param[1:]))
    main(param[1:])

