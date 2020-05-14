# import json

import requests
import time
import random

from bs4 import BeautifulSoup as Soup
# from pymongo import MongoClient as Client
import threading

from tools.db import MysqlConn
from tools.settings import MySQL_INFO


def parse_items(response):
    # 存放ip信息字典的列表
    soup = Soup(response.text, 'lxml')
    # 第一个是显示最上方的信息的，需要丢掉
    items = soup.find_all('tr')[1:]
    ips = []
    for tr in items:
        tds = tr.find_all('td')
        ip = {
            'ip': tds[1].get_text(),
            'port': tds[2].get_text(),
            'proxy_type': tds[5].get_text().lower(),
            'speed': float(tds[7].div['title'][:-1]),
        }
        ips.append(ip)
    return ips


# def write_to_json(ips, file_dir='proxies.json'):
#     with open(file_dir, 'w', encoding='utf-8') as f:
#         json.dump(ips, f, indent=4)


# def write_to_json(ips, file_dir='proxies.json'):
#     try:
#         with open(file_dir, 'r', encoding='utf-8') as f1:
#             result = json.loads(f1.read())
#         for each_ip in ips:
#             if each_ip not in result:
#                 result.append(each_ip)
#     except:
#         result = ips
#     with open(file_dir, 'w', encoding='utf-8') as f2:
#         f2.write(json.dumps(result, ensure_ascii=False))


# def write_to_mongo(ips):
#     '''将数据写入mongoDB'''
#     client = Client(host='localhost', port=27017)
#     db = client['proxies_db']
#     coll = db['proxies']
#     # 先检测，再写入，防止重复
#     for ip in ips:
#         if coll.find({'ip': ip['ip']}).count() == 0:
#             coll.insert_one(ip)
#     client.close()


class GoodProxies(object):

    def __init__(self, headers=None):
        self.db = MysqlConn(**MySQL_INFO)
        self.headers = headers

    def dict2proxy(self, dic):
        s = dic['proxy_type'] + '://' + dic['ip'] + ':' + str(dic['port'])
        print({'http': s, 'https': s})
        return {'http': s, 'https': s}

    def add(self, proxy_info):
        if self.judge_ip(proxy_info):
            sql = "insert proxy_ip(ip,port,speed,proxy_type) " \
                  "VALUES('{ip}','{port}',{speed},'{proxy_type}')".format(**proxy_info)
            self.db.read(sql)

    def delete(self, ip):
        delete_sql = "delete from proxy_ip where ip = '{0}'".format(ip)
        self.db.read(delete_sql)

    def delete_all(self):
        # 任务闲置过久IP池可能已经腐败，需要清除重下
        delete_sql = "delete from proxy_ip"
        self.db.read(delete_sql)

    def get_random_ip(self):
        # 在获取IP时，可以验证一下剩余IP数量，在必要时重新扩充IP池
        # 从数据库中随机获取一个可用ip
        random_sql = 'SELECT ip, port, proxy_type FROM proxy_ip ORDER BY RAND() LIMIT 1'
        random_ip = self.db.read(random_sql)
        if len(random_ip) == 0:
            # 此处可以加一个重新下载IP池的动作，但一定要注意多进程时限制该动作只能有一个进程执行
            raise Exception('没有可用IP,请重新建立IP池.')
        for ip_info in random_ip:
            if self.judge_ip(ip_info):
                return self.dict2proxy(ip_info)
            else:
                return self.get_random_ip()

    def judge_ip(self, proxy_info):
        pro = self.dict2proxy(proxy_info)
        # print(pro)
        try:
            url = 'https://www.ipip.net/'
            r = requests.get(url, headers=self.headers, proxies=pro, timeout=5)
            r.raise_for_status()
            print(r.status_code, proxy_info['ip'])
        except Exception as e:
            print('该IP不可用: %s ERROR: %s' % (pro, str(e)))
            return False
        else:
            return True


class GetThread(threading.Thread):
    '''对Thread进行封装'''
    def __init__(self, args):
        threading.Thread.__init__(self, args=args)
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Chrome/64.0.3282.186 Safari/537.36'}
        self.good_proxies = GoodProxies(self.headers)

    def run(self):
        url = 'http://www.xicidaili.com/nt/%d' % self._args[0]
        # 发起网络访问
        # 这里会尝试使用IP池访问，获取IP池，获取不到时会不使用IP池，尽可能避免本地IP池被封
        try:
            pro = self.good_proxies.get_random_ip()
            r = requests.get(url, headers=self.headers, proxies=pro)
        except:
            r = requests.get(url, headers=self.headers)
        r.encoding = r.apparent_encoding
        r.raise_for_status()
        ips = parse_items(r)
        threads = []
        for ip in ips:
            # 开启多线程
            t = threading.Thread(target=self.good_proxies.add, args=(ip,))
            t.start()
            time.sleep(random.random() * 0.8 + 0.2)
            threads.append(t)
        [t.join() for t in threads]

    def get_result(self):
        return self.good_proxies


def get_proxies(ip_page=3):  # file_dir='proxies.json',
    # 主函数使用多线程
    # 可以将该任务做成定时任务，定期获取IP池，作为解决IP池持久使用的办法
    threads = []
    for i in range(1, ip_page):
        t = GetThread(args=(i, ))
        t.start()
        time.sleep(10)
        threads.append(t)
    [t.join() for t in threads]
    # proxies = []
    # for t in threads:
    #     # write_to_mongo(t.get_result())
    #     proxies.extend(t.get_result())
    # write_to_json(proxies, file_dir)


if __name__ == '__main__':
    # gp = GoodProxies()
    # print(gp.get_random_ip())
    get_proxies(ip_page=3)
