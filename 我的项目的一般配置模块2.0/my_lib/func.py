# -*- coding:utf-8 -*-
import os
import shutil
import glob
import zipfile
import re
import json
import random
import difflib
import tempfile
import subprocess
import logging

import requests
from bs4 import BeautifulSoup
from win32com import client as wc
import pywintypes

import pandas as pd


class MyReBase(object):
    """自定义正则规则库基础类，待扩充"""
    @property
    def re_rules(self):
        return []

    def search(self, string: str, *args, **kwargs):
        result = None
        for re_rule in self.re_rules:
            result = re_rule.search(string, *args, **kwargs)
            if result is not None:
                return result
        return result


class TrieNode(object):
    """字典树, 可存储信息"""
    def __init__(self):
        self.nodes = dict()  # 构建字典
        self.is_leaf = False
        self.info=None

    def set_info(self, info):
        self.info = info

    def insert(self, word: str, info=None):
        curr = self
        for char in word:
            if char not in curr.nodes:
                curr.nodes[char] = TrieNode()
            curr = curr.nodes[char]
        curr.is_leaf = True
        curr.set_info(info)

    def insert_many(self, words: [str], infos=None):
        if infos is None:
            infos = [None for _ in words]
        for word, info in zip(words, infos):
            self.insert(word, info)

    def _search(self, word: str):
        curr = self
        for char in word:
            if char not in curr.nodes:
                return None
            curr = curr.nodes[char]
        return curr

    def search(self, word: str):
        curr = self._search(word)
        if curr is None:
            return False
        return curr.is_leaf

    def search_info(self, word: str):
        curr = self._search(word)
        if curr is None:
            return None
        return curr.info

    def match(self, word: str, speed=True):
        curr = self
        result = ['', word]
        for n, char in enumerate(word, 0):
            if char not in curr.nodes:
                return result
            curr = curr.nodes[char]
            if curr.is_leaf:
                if speed:
                    result = word[:n + 1], word[n + 1:]
                else:
                    return [word[:n+1], word[n+1:]]
        return result
		

class TrieNode(object):
    """字典树"""
    def __init__(self):
        self.nodes = dict()  # 构建字典
        self.is_leaf = False

    def insert(self, word: str):
        curr = self
        for char in word:
            if char not in curr.nodes:
                curr.nodes[char] = TrieNode()
            curr = curr.nodes[char]
        curr.is_leaf = True

    def insert_many(self, words: [str]):
        for word in words:
            self.insert(word)

    def search(self, word: str):
        curr = self
        for char in word:
            if char not in curr.nodes:
                return False
            curr = curr.nodes[char]
        return curr.is_leaf

    def match(self, word: str, speed=True):
        curr = self
        result = ['', word]
        for n, char in enumerate(word, 0):
            if char not in curr.nodes:
                return result
            curr = curr.nodes[char]
            if curr.is_leaf:
                if speed:
                    result = word[:n + 1], word[n + 1:]
                else:
                    return [word[:n+1], word[n+1:]]
        return result

# -------------网络爬虫----------------------


def get_soup(url, *args, **kwargs):
    html = requests.get(url, *args, **kwargs)
    return BeautifulSoup(html.content, 'lxml')


# -------------文件处理----------------------


class MyJSON(object):
    """以行字符串的形式逐行存储，以json格式逐行读取"""
    def __init__(self, f_path):
        self.f_path = f_path

    def init(self):
        if os.path.isfile(self.f_path):
            data = self.read_json()
            return data
        f_dir = os.path.dirname(self.f_path)
        if f_dir != '' and not os.path.isdir(f_dir):
            # 没有文件存储路径建立一个
            os.makedirs(os.path.dirname(self.f_path))
        return None

    def read_json(self):
        with open(self.f_path, "r", encoding='utf-8') as f:
            data = f.read()
        if data == "":
            return None
        return json.loads(data)

    def write_json(self, data):
        with open(self.f_path, "w", encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=1))
        return self


class MyJSON2(object):
    """以行字符串的形式逐行存储，以json格式逐行读取"""
    def __init__(self, f_path):
        self.f_path = f_path

    def json2str(self, data):
        return json.dumps(data, ensure_ascii=False) + '\n'

    def addline(self, data):
        """未经处理的列表"""
        self.addline_str(self.json2str(data))

    def addline_str(self, data):
        """已处理成json格式的"""
        with open(self.f_path, "a", encoding='utf-8') as f:
            f.write(data)

    def read_json(self):
        with open(self.f_path, "r", encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            yield json.loads(line)

    def pop(self, n=-1):
        with open(self.f_path, "r", encoding='utf-8') as f1:
            lines = f1.readlines()
        with open(self.f_path, "w", encoding='utf-8') as f2:
            if n == -1:
                f2.writelines(lines[:n])
            else:
                f2.writelines(lines[:n]+lines[n+1:])
        return json.loads(lines[n])

    def len(self):
        with open(self.f_path, "r", encoding='utf-8') as f1:
            lines = [i for i in f1.readlines() if i.strip() != ""]
        return len(lines)

    def covered_writing(self, lines):
        """
        覆盖写入，用新内容覆盖旧的内容，
        可以应用于修改时，对文件内容进行了修改，之后重写写回文件中
        """
        lines_str = "".join([self.json2str(line) for line in lines])
        with open(self.f_path, "w", encoding='utf-8') as f:
            f.write(lines_str)
        logging.info('替换成功：%d行' % len(lines))


class MyJSON3(MyJSON2):
    """带结果集切片功能的数据处理类，继承于MyJson2的方法有些并未重写，因此功能可能与想象的不同，不建议使用"""

    def __init__(self, f_path, max_line=10000):
        """
        :param f_path: 文件名
        :param max_line: 文件最多多少行数据
        """
        self.begin = self.num = 0  # 当前文件储存的是开始与第几条的、当前文件中已经存储了多少条
        self.max_line = max_line
        self.f_dir, self.f_name = os.path.split(f_path)
        self.fname, self.suffix = os.path.splitext(self.f_name)
        self.re_fname = re.compile(self.fname + r'-(\d+)-(\d+)')
        self.init_begin()
        super(MyJSON3, self).__init__(self.get_f_path())
        self.init_num()  # 执行时需要有初始化了的f_path,之后f_path的初始化有其掌握

    def get_max_line_fname(self):
        return os.path.join(self.fname + "-%d-%d" % (self.begin, self.begin + self.max_line))

    def get_f_path(self):
        return os.path.join(self.f_dir, self.get_max_line_fname() + self.suffix)

    def init_begin(self):
        for f_name in os.listdir(self.f_dir):
            result = self.re_fname.search(f_name)
            if result is not None:
                begin, end = result.groups()
                if int(begin) > self.begin:
                    self.begin = int(begin)

    def init_num(self):
        if not os.path.isfile(self.get_f_path()):
            self.num = 0
        else:
            self.num = self.len()

    def judge_full(self):
        if self.num >= self.max_line:
            self.num = 0
            self.begin += self.max_line
            self.f_path = self.get_f_path()

    def addline(self, data):
        self.judge_full()
        super(MyJSON3, self).addline(data)
        self.num += 1


def loads(string, strict=True, *args, **kwargs):
	"""json的loads方法的重写，可以处理不同语言之间切换导致的反斜杠使用问题"""
    re_error = re.compile(r"Invalid \\escape: line \d+ column \d+ \(char (\d+)\)")
    try:
        dict_infos = json.loads(string, strict=strict, *args, **kwargs)
    except json.decoder.JSONDecodeError as e:
        error_info = re_error.search(e.__str__())
        if error_info is not None:
            key = int(error_info.groups()[0])
            return loads(string[:key]+string[key+1:], strict=strict, *args, **kwargs)
        else:
            raise e
    return dict_infos


def get_doc(doc_file, word, remove_doc=False, retry=True):
    try:
        doc = word.Documents.Open(doc_file, 'r')  # 只读格式打开，可以防止某些需要输入密码才可以编辑的文档打不开
    except pywintypes.com_error as e:
        if not retry:
            if remove_doc:
                os.remove(doc_file)
                logger.info("中转的doc文件已被删除：%s" % doc_file)
            raise e
        f_base, f_suffix = os.path.splitext(doc_file)  # 分离文件名和后缀名
        tmpfd2, temp_doc = tempfile.mkstemp(suffix=f_suffix)
        logger.info("创建中转的doc文件：%s" % temp_doc)
        os.close(tmpfd2)
        mycopyfile(doc_file, temp_doc)
        return get_doc(temp_doc, word, remove_doc=True, retry=False)
    tmpfd, temp_docx = tempfile.mkstemp(suffix='.docx')
    os.close(tmpfd)
    # doc.SaveAs(temp_docx, 12)
    doc.SaveAs(temp_docx, 12, False, "", True, "", False, False, False, False)
    doc.Close()
    if remove_doc:
        os.remove(doc_file)
        logger.info("中转的doc文件已被删除：%s" % doc_file)
    return temp_docx


def doc2docx(doc_file):
    """
    将doc格式的文件转为docx, 建议在docx_file处设置为系统默认临时文件夹，
    防止处理过程导致文件生成并无法删除, 事后应删除中间文件
    """
    word = wc.Dispatch("Word.Application")
    temp_docx = get_doc(doc_file, word)
    word.Quit()
    logger.info('doc to docx success: %s' % temp_docx)
    return temp_docx


def doc2docx1(doc_file, docx_file=None):
    """将doc格式的文件转为docx"""
    word = wc.Dispatch("Word.Application")
    doc = word.Documents.Open(doc_file, 'r')  # 只读格式打开，可以防止某些需要输入密码才可以编辑的文档打不开
    if docx_file is None:
        docx_file = os.path.splitext(doc_file)[0] + '.docx'
    fpath, fname = os.path.split(docx_file)  # 分离文件名和路径
    if not os.path.exists(fpath):
        os.makedirs(fpath)  # 创建路径
    doc.SaveAs(docx_file, 12)
    doc.Close()
    word.Quit()
    print('doc to docx success!')
    return docx_file


def doc2docx2(doc_file):
    """
    将doc格式的文件转为docx, docx_file处设置为系统默认临时文件夹，
    防止处理过程导致文件生成并无法删除,
    使用完别忘了使用os.remove(tempfilename)删除中间文件
    """
    word = wc.Dispatch("Word.Application")
    doc = word.Documents.Open(doc_file, 'r')  # 只读格式打开，可以防止某些需要输入密码才可以编辑的文档打不开
    tmpfd, tempfilename = tempfile.mkstemp(suffix='.docx')
    os.close(tmpfd)
    # docx_file = os.path.splitext(doc_file)[0] + '.docx'
    # fpath, fname = os.path.split(docx_file)  # 分离文件名和路径
    # docx_file = os.path.join(tempfilename, fname)
    doc.SaveAs(tempfilename, 12)
    doc.Close()
    word.Quit()
    print('doc to docx success:' % tempfilename)
    return tempfilename


def get_child_dirs(dsc_dir):
    """
    :param dsc_dir: 要处理的目录
    :return: 子目录的目录名与子目录的路径
    """
    child_dirs = {}
    for child_dir in os.listdir(dsc_dir):
        abs_child_dir = os.path.join(dsc_dir, child_dir)
        if os.path.isdir(abs_child_dir):
            child_dirs[child_dir] = abs_child_dir
    return child_dirs


def get_files(file_dir, second=''):
    """轮训获取路径下的所有文件，会自动查询进一步的路径并返回拼接后的相对路径文件名"""
    for f in os.listdir(file_dir):
        if os.path.isdir(os.path.join(file_dir, f)):
            for i in get_files(os.path.join(file_dir, f), os.path.join(second, f)):
                yield i
        else:
            yield os.path.join(second, f)


def mymovefile(srcfile, dstfile):
    """移动文件"""
    if not os.path.isfile(srcfile):
        print("%s not exist!" % srcfile)
    else:
        fpath, fname = os.path.split(dstfile)  # 分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)  # 创建路径
        shutil.move(srcfile, dstfile)  # 移动文件
        print("move %s -> %s" % (srcfile, dstfile))


def mycopyfile(srcfile, dstfile):
    """复制文件"""
    if not os.path.isfile(srcfile):
        print("%s not exist!" % srcfile)
    else:
        fpath, fname = os.path.split(dstfile)  # 分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)  # 创建路径
        shutil.copyfile(srcfile, dstfile)  # 复制文件
        print("copy %s -> %s" % (srcfile, dstfile))


def mycopypath(src_path, dst_path):
    """复制文件夹"""
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)

    if os.path.exists(src_path):
        # root 所指的是当前正在遍历的这个文件夹的本身的地址
        # dirs 是一个 list，内容是该文件夹中所有的目录的名字(不包括子目录)
        # files 同样是 list, 内容是该文件夹中所有的文件(不包括子目录)
        for root, dirs, files in os.walk(src_path):
            for file in files:
                src_file = os.path.join(root, file)
                shutil.copy(src_file, dst_path)
                print(src_file)


def unzip_file(dir_path, unzip_file_path):
    """
    :param dir_path: 需要解压的文件
    :param unzip_file_path: 解压后存储路径
    :return:
    """
    # 找到压缩文件夹
    dir_list = glob.glob(dir_path)
    if dir_list:
        # 循环zip文件夹
        for dir_zip in dir_list:
            # 以读的方式打开
            with zipfile.ZipFile(dir_zip, 'r') as f:
                for file in f.namelist():
                    f.extract(file, path=unzip_file_path)
            os.remove(dir_zip)


def zip_files(dir_path, zip_path):
    """ 压缩文件夹下的所有文件（会拆出目录结构）
    :param dir_path: 需要压缩的文件目录
    :param zip_path: 压缩后的目录
    :return:
    """
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as f:
        for root, _, file_names in os.walk(dir_path):
            for filename in file_names:
                f.write(os.path.join(root, filename), filename)


def zip_dir(dir_path, zip_path):
    """
    压缩指定文件夹
    :param dir_path: 目标文件夹路径
    :param zip_path: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    zip = zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dir_path):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(dir_path, '')

        for filename in filenames:
            zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
    zip.close()


def del_path(f_path, keep_root=False):
    """删除文件或目录"""
    if os.path.isfile(f_path):
        os.remove(f_path)
    elif os.path.isdir(f_path):
        shutil.rmtree(f_path)
        if keep_root:
            os.makedirs(f_path)
    else:
        raise FileNotFoundError("文件或路径不存在：%s" % f_path)


def del_null_dir(f_dir):
    """删除文件夹下的所有空路径"""
    del_dir = True
    list_dir = os.listdir(f_dir)
    for i in list_dir:
        child_dir = os.path.join(f_dir, i)
        if os.path.isfile(child_dir):
            del_dir = False
            continue
        elif not del_null_dir(child_dir):
            del_dir = False
    if del_dir:
        print("删除空路径：%s" % f_dir)
        if os.path.isdir(f_dir):
            os.removedirs(f_dir)
    return del_dir
				

def save_file(data, file, mode='w'):
    """保存文件"""
    fpath, fname = os.path.split(file)  # 分离文件名和路径
    if not os.path.exists(fpath):
        os.makedirs(fpath)  # 创建路径
    with open(file, mode) as f:
        f.write(data)
    print("save file %s" % file)


def join_url(host, path, *args):
    """合成url"""
    if host[-1] == '/' and path[0] == '/':
        path = path[1:]
    elif host[-1] != '/' and path[0] != '/':
        host += '/'
    host = host + path
    if len(args) != 0:
        return join_url(host, *args)
    return host


def href2url(href, host=''):
    """从href转换成url"""
    re_url = re.compile(r'^https*://')
    re_local = re.compile(r'^#')
    re_href = re.compile(r'(\.\./)*\.*\.*(/.*)')
    href = href.strip()
    if re_url.search(href):
        return href
    elif re_local.search(href):
        return None
    else:
        try:
            href = re_href.findall(href)[0][1]
        except IndexError:
            pass
            # print('链接格式不正常，链接后缀：%s' % href)
        return join_url(host, href)


def rep_spetial_char(fname, rep='_'):
    """将文件名中的特殊字符替换为指定字符"""
    return re.sub(r'[\\/:*?"<>|\n\t\r]', rep, fname)


def rep_spetial_char2(fdir, rep='_'):
    """将带路径的文件或路径中的特殊字符替换为指定字符"""
    return re.sub(r'[:*?"<>|\n\t\r]', rep, fdir)


def rep_spetial_char3(fdir, rep='_'):
    """将带路径的文件或路径中的特殊字符替换为指定字符,针对Windows下的路径进行特殊处理
    认为磁盘名都为一个字母+冒号的格式
    """
    if re.search(r'[A-Za-z]:', fdir[:2]) is not None:
        disk = fdir[:2]
        fdir = fdir[2:]
        return disk + rep_spetial_char2(fdir, rep)
    return rep_spetial_char2(fdir, rep)


def dir2long(f_dir, update, other_long=0, long_max=244-10):
    """ 全部路径不能超过244, other_long时注意路径结尾有一个斜杠最好不要忽略，或者多算几位
    DIR_LONG_MAX = 259
    FNAME_LONG_MAX = 255
    PATH_LONG_MAX = 244
    :param f_dir: 文件路径
    :param update: 需要更新的位置
    :param other_long: 如果是相对路径，这里填入相对于的那个路径的字符数
    :param long_max: 全路径最大长度,默认为路径最大长度-10,路径最长为244个字符
    :return:
    """
    n = long_max - other_long - len(f_dir)
    if n < 0:
        f_dir = f_dir.replace(update, update[:n-3]+'。。。')
    return f_dir


def sh(command):
    """调用系统命令，并实时输出日志"""
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    lines = []
    for line in iter(p.stdout.readline, b''):
        line = line.strip().decode("GB2312")
        print(line)
        lines.append(line)
    return lines


class Other(object):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # 本级目录
    ROOT_DIR_P = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # 上级目录
    fdir, fname = os.path.split('/home/test/aaa.txt')  # 分离文件名和路径
    f_base, f_suffix = os.path.splitext(fname)  # 分离文件名和后缀名
    os.path.exists('/home/test')  # 判断路径是否存在
    # dir(class)  # 返回类的全部属性
    # 查看类的所有自定义方法, object改为确定的类
    func_name = (list(filter(lambda m: not m.startswith("__") and not m.endswith(
        "__") and callable(getattr(object, m)), dir(object))))
    # 创建临时文件
    tmpfd, tempfilename = tempfile.mkstemp(suffix='.docx')
    os.close(tmpfd)
    # 简繁对照表
    zh_s = '皑蔼碍爱翱袄奥坝罢摆败颁办绊帮绑镑谤剥饱宝报鲍辈贝钡狈备惫绷笔毕毙闭边编贬变辩辫鳖瘪濒滨宾摈饼拨钵铂驳卜补参蚕残惭惨灿苍舱仓沧厕侧册测层诧搀掺蝉馋谗缠铲产阐颤场尝长偿肠厂畅钞车彻尘陈衬撑称惩诚骋痴迟驰耻齿炽冲虫宠畴踌筹绸丑橱厨锄雏础储触处传疮闯创锤纯绰辞词赐聪葱囱从丛凑窜错达带贷担单郸掸胆惮诞弹当挡党荡档捣岛祷导盗灯邓敌涤递缔点垫电淀钓调迭谍叠钉顶锭订东动栋冻斗犊独读赌镀锻断缎兑队对吨顿钝夺鹅额讹恶饿儿尔饵贰发罚阀珐矾钒烦范贩饭访纺飞废费纷坟奋愤粪丰枫锋风疯冯缝讽凤肤辐抚辅赋复负讣妇缚该钙盖干赶秆赣冈刚钢纲岗皋镐搁鸽阁铬个给龚宫巩贡钩沟构购够蛊顾剐关观馆惯贯广规硅归龟闺轨诡柜贵刽辊滚锅国过骇韩汉阂鹤贺横轰鸿红后壶护沪户哗华画划话怀坏欢环还缓换唤痪焕涣黄谎挥辉毁贿秽会烩汇讳诲绘荤浑伙获货祸击机积饥讥鸡绩缉极辑级挤几蓟剂济计记际继纪夹荚颊贾钾价驾歼监坚笺间艰缄茧检碱硷拣捡简俭减荐槛鉴践贱见键舰剑饯渐溅涧浆蒋桨奖讲酱胶浇骄娇搅铰矫侥脚饺缴绞轿较秸阶节茎惊经颈静镜径痉竞净纠厩旧驹举据锯惧剧鹃绢杰洁结诫届紧锦仅谨进晋烬尽劲荆觉决诀绝钧军骏开凯颗壳课垦恳抠库裤夸块侩宽矿旷况亏岿窥馈溃扩阔蜡腊莱来赖蓝栏拦篮阑兰澜谰揽览懒缆烂滥捞劳涝乐镭垒类泪篱离里鲤礼丽厉励砾历沥隶俩联莲连镰怜涟帘敛脸链恋炼练粮凉两辆谅疗辽镣猎临邻鳞凛赁龄铃凌灵岭领馏刘龙聋咙笼垄拢陇楼娄搂篓芦卢颅庐炉掳卤虏鲁赂禄录陆驴吕铝侣屡缕虑滤绿峦挛孪滦乱抡轮伦仑沦纶论萝罗逻锣箩骡骆络妈玛码蚂马骂吗买麦卖迈脉瞒馒蛮满谩猫锚铆贸么霉没镁门闷们锰梦谜弥觅绵缅庙灭悯闽鸣铭谬谋亩钠纳难挠脑恼闹馁腻撵捻酿鸟聂啮镊镍柠狞宁拧泞钮纽脓浓农疟诺欧鸥殴呕沤盘庞国爱赔喷鹏骗飘频贫苹凭评泼颇扑铺朴谱脐齐骑岂启气弃讫牵扦钎铅迁签谦钱钳潜浅谴堑枪呛墙蔷强抢锹桥乔侨翘窍窃钦亲轻氢倾顷请庆琼穷趋区躯驱龋颧权劝却鹊让饶扰绕热韧认纫荣绒软锐闰润洒萨鳃赛伞丧骚扫涩杀纱筛晒闪陕赡缮伤赏烧绍赊摄慑设绅审婶肾渗声绳胜圣师狮湿诗尸时蚀实识驶势释饰视试寿兽枢输书赎属术树竖数帅双谁税顺说硕烁丝饲耸怂颂讼诵擞苏诉肃虽绥岁孙损笋缩琐锁獭挞抬摊贪瘫滩坛谭谈叹汤烫涛绦腾誊锑题体屉条贴铁厅听烃铜统头图涂团颓蜕脱鸵驮驼椭洼袜弯湾顽万网韦违围为潍维苇伟伪纬谓卫温闻纹稳问瓮挝蜗涡窝呜钨乌诬无芜吴坞雾务误锡牺袭习铣戏细虾辖峡侠狭厦锨鲜纤咸贤衔闲显险现献县馅羡宪线厢镶乡详响项萧销晓啸蝎协挟携胁谐写泻谢锌衅兴汹锈绣虚嘘须许绪续轩悬选癣绚学勋询寻驯训讯逊压鸦鸭哑亚讶阉烟盐严颜阎艳厌砚彦谚验鸯杨扬疡阳痒养样瑶摇尧遥窑谣药爷页业叶医铱颐遗仪彝蚁艺亿忆义诣议谊译异绎荫阴银饮樱婴鹰应缨莹萤营荧蝇颖哟拥佣痈踊咏涌优忧邮铀犹游诱舆鱼渔娱与屿语吁御狱誉预驭鸳渊辕园员圆缘远愿约跃钥岳粤悦阅云郧匀陨运蕴酝晕韵杂灾载攒暂赞赃脏凿枣灶责择则泽贼赠扎札轧铡闸诈斋债毡盏斩辗崭栈战绽张涨帐账胀赵蛰辙锗这贞针侦诊镇阵挣睁狰帧郑证织职执纸挚掷帜质钟终种肿众诌轴皱昼骤猪诸诛烛瞩嘱贮铸筑驻专砖转赚桩庄装妆壮状锥赘坠缀谆浊兹资渍踪综总纵邹诅组钻致钟么为只凶准启板里雳余链泄'
    zh_t = '皚藹礙愛翺襖奧壩罷擺敗頒辦絆幫綁鎊謗剝飽寶報鮑輩貝鋇狽備憊繃筆畢斃閉邊編貶變辯辮鼈癟瀕濱賓擯餅撥缽鉑駁蔔補參蠶殘慚慘燦蒼艙倉滄廁側冊測層詫攙摻蟬饞讒纏鏟産闡顫場嘗長償腸廠暢鈔車徹塵陳襯撐稱懲誠騁癡遲馳恥齒熾沖蟲寵疇躊籌綢醜櫥廚鋤雛礎儲觸處傳瘡闖創錘純綽辭詞賜聰蔥囪從叢湊竄錯達帶貸擔單鄲撣膽憚誕彈當擋黨蕩檔搗島禱導盜燈鄧敵滌遞締點墊電澱釣調叠諜疊釘頂錠訂東動棟凍鬥犢獨讀賭鍍鍛斷緞兌隊對噸頓鈍奪鵝額訛惡餓兒爾餌貳發罰閥琺礬釩煩範販飯訪紡飛廢費紛墳奮憤糞豐楓鋒風瘋馮縫諷鳳膚輻撫輔賦複負訃婦縛該鈣蓋幹趕稈贛岡剛鋼綱崗臯鎬擱鴿閣鉻個給龔宮鞏貢鈎溝構購夠蠱顧剮關觀館慣貫廣規矽歸龜閨軌詭櫃貴劊輥滾鍋國過駭韓漢閡鶴賀橫轟鴻紅後壺護滬戶嘩華畫劃話懷壞歡環還緩換喚瘓煥渙黃謊揮輝毀賄穢會燴彙諱誨繪葷渾夥獲貨禍擊機積饑譏雞績緝極輯級擠幾薊劑濟計記際繼紀夾莢頰賈鉀價駕殲監堅箋間艱緘繭檢堿鹼揀撿簡儉減薦檻鑒踐賤見鍵艦劍餞漸濺澗漿蔣槳獎講醬膠澆驕嬌攪鉸矯僥腳餃繳絞轎較稭階節莖驚經頸靜鏡徑痙競淨糾廄舊駒舉據鋸懼劇鵑絹傑潔結誡屆緊錦僅謹進晉燼盡勁荊覺決訣絕鈞軍駿開凱顆殼課墾懇摳庫褲誇塊儈寬礦曠況虧巋窺饋潰擴闊蠟臘萊來賴藍欄攔籃闌蘭瀾讕攬覽懶纜爛濫撈勞澇樂鐳壘類淚籬離裏鯉禮麗厲勵礫曆瀝隸倆聯蓮連鐮憐漣簾斂臉鏈戀煉練糧涼兩輛諒療遼鐐獵臨鄰鱗凜賃齡鈴淩靈嶺領餾劉龍聾嚨籠壟攏隴樓婁摟簍蘆盧顱廬爐擄鹵虜魯賂祿錄陸驢呂鋁侶屢縷慮濾綠巒攣孿灤亂掄輪倫侖淪綸論蘿羅邏鑼籮騾駱絡媽瑪碼螞馬罵嗎買麥賣邁脈瞞饅蠻滿謾貓錨鉚貿麽黴沒鎂門悶們錳夢謎彌覓綿緬廟滅憫閩鳴銘謬謀畝鈉納難撓腦惱鬧餒膩攆撚釀鳥聶齧鑷鎳檸獰甯擰濘鈕紐膿濃農瘧諾歐鷗毆嘔漚盤龐國愛賠噴鵬騙飄頻貧蘋憑評潑頗撲鋪樸譜臍齊騎豈啓氣棄訖牽扡釺鉛遷簽謙錢鉗潛淺譴塹槍嗆牆薔強搶鍬橋喬僑翹竅竊欽親輕氫傾頃請慶瓊窮趨區軀驅齲顴權勸卻鵲讓饒擾繞熱韌認紉榮絨軟銳閏潤灑薩鰓賽傘喪騷掃澀殺紗篩曬閃陝贍繕傷賞燒紹賒攝懾設紳審嬸腎滲聲繩勝聖師獅濕詩屍時蝕實識駛勢釋飾視試壽獸樞輸書贖屬術樹豎數帥雙誰稅順說碩爍絲飼聳慫頌訟誦擻蘇訴肅雖綏歲孫損筍縮瑣鎖獺撻擡攤貪癱灘壇譚談歎湯燙濤縧騰謄銻題體屜條貼鐵廳聽烴銅統頭圖塗團頹蛻脫鴕馱駝橢窪襪彎灣頑萬網韋違圍爲濰維葦偉僞緯謂衛溫聞紋穩問甕撾蝸渦窩嗚鎢烏誣無蕪吳塢霧務誤錫犧襲習銑戲細蝦轄峽俠狹廈鍁鮮纖鹹賢銜閑顯險現獻縣餡羨憲線廂鑲鄉詳響項蕭銷曉嘯蠍協挾攜脅諧寫瀉謝鋅釁興洶鏽繡虛噓須許緒續軒懸選癬絢學勳詢尋馴訓訊遜壓鴉鴨啞亞訝閹煙鹽嚴顔閻豔厭硯彥諺驗鴦楊揚瘍陽癢養樣瑤搖堯遙窯謠藥爺頁業葉醫銥頤遺儀彜蟻藝億憶義詣議誼譯異繹蔭陰銀飲櫻嬰鷹應纓瑩螢營熒蠅穎喲擁傭癰踴詠湧優憂郵鈾猶遊誘輿魚漁娛與嶼語籲禦獄譽預馭鴛淵轅園員圓緣遠願約躍鑰嶽粵悅閱雲鄖勻隕運蘊醞暈韻雜災載攢暫贊贓髒鑿棗竈責擇則澤賊贈紮劄軋鍘閘詐齋債氈盞斬輾嶄棧戰綻張漲帳賬脹趙蟄轍鍺這貞針偵診鎮陣掙睜猙幀鄭證織職執紙摯擲幟質鍾終種腫衆謅軸皺晝驟豬諸誅燭矚囑貯鑄築駐專磚轉賺樁莊裝妝壯狀錐贅墜綴諄濁茲資漬蹤綜總縱鄒詛組鑽緻鐘麼為隻兇準啟闆裡靂餘鍊洩'


# -------------好用算法----------------------
class IntBining(object):
    """一个int型的分箱模块，传入箱的大小，自动分箱"""
    def __init__(self, end, begin=0, box_num=10, bin_type="simple"):
        """
        :param end:
        :param begin:
        :param box_num:
        :param bin_type: simple, even
        """
        assert end - begin >= box_num
        bins = {
            "simple": self.simple_bins,
            "even": self.even_bins,
        }
        self.end = end
        self.begin = begin
        self.box_num = int(box_num)
        self.bin = bins[bin_type](self.end, begin=self.begin, box_num=self.box_num)

    def simple_bins(self, end, begin=0, box_num=10):
        """最后一个箱中承担多出的所有数据"""
        my_len = (end - begin) // box_num
        result = []
        begin_ = begin
        for i in range(1, box_num + 1):
            end_ = my_len + begin_
            result.append([begin_, end_])
            begin_ = end_
        result[-1][-1] = end
        return result

    def even_bins(self, end, begin=0, box_num=10):
        """均匀的分箱，保证分箱后的数据数量差小于1"""
        my_len = (end - begin) // box_num
        my_remain = (end - begin) % box_num
        result = []
        begin_ = begin
        for i in range(1, box_num + 1):
            if i <= my_remain:
                end_ = begin_ + my_len + 1
            else:
                end_ = begin_ + my_len
            result.append([begin_, end_])
            begin_ = end_
        result[-1][-1] = end
        return result

    def str(self):
        return ["(%d, %d]" % (begin, end) for begin, end in self.bin]

    def __len__(self):
        return len(self.bin)

    def __getitem__(self, item):
        n = self.box_num // 2
        while True:
            assert n >= 0
            if item <= self.bin[n][0]:
                n -= 1
            elif item > self.bin[n][1]:
                n += 1
            else:
                return n

    def __call__(self, n=None, *args, **kwargs):
        return self.bin[n]
    """一个int型的分箱模块，传入箱的大小，自动分箱"""
    def __init__(self, end, begin=0, box_num=10, bin_type="simple"):
        """
        :param end:
        :param begin:
        :param box_num:
        :param bin_type: simple, even
        """
        assert end - begin >= box_num
        bins = {
            "simple": self.simple_bins,
            "even": self.even_bins,
        }
        self.end = end
        self.begin = begin
        self.box_num = int(box_num)
        self.bin = bins[bin_type](self.end, begin=self.begin, box_num=self.box_num)

    def simple_bins(self, end, begin=0, box_num=10):
        """最后一个箱中承担多出的所有数据"""
        my_len = (end - begin) // box_num
        result = []
        begin_ = begin
        for i in range(1, box_num + 1):
            end_ = my_len + begin_
            result.append([begin_, end_])
            begin_ = end_
        result[-1][-1] = end
        return result

    def even_bins(self, end, begin=0, box_num=10):
        """均匀的分箱，保证分箱后的数据数量差小于1"""
        my_len = (end - begin) // box_num
        my_remain = (end - begin) % box_num
        result = []
        begin_ = begin
        for i in range(1, box_num + 1):
            if i <= my_remain:
                end_ = begin_ + my_len + 1
            else:
                end_ = begin_ + my_len
            result.append([begin_, end_])
            begin_ = end_
        result[-1][-1] = end
        return result

    def str(self):
        return ["[%d, %d)" % (begin, end) for begin, end in self.bin]

    def __len__(self):
        return len(self.bin)

    def __getitem__(self, item):
        n = self.box_num // 2
        while True:
            assert n >= 0
            if item < self.bin[n][0]:
                n -= 1
            elif item >= self.bin[n][1]:
                n += 1
            else:
                return n

    def __call__(self, n=None, *args, **kwargs):
        return self.bin[n]
		

def random_bining(data: list, xiang=5):
    """将数据随机分成N分"""
    data_ = data[:]
    random.shuffle(data_)
    result = []
    for begin, end in bining1(len(data_), xiang=xiang):
        result.append(data_[begin:end])
    return result


def zh_num(n):
    """数字转中文数字"""
    zh_n = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九"]
    zh_n2 = ["十", "百"]
    result = ""
    i = 0
    while True:
        zheng, yu = n // 10, n % 10
        if i == 0:
            if yu == 0:
                pass
            else:
                result = zh_n[yu] + result
        elif i == 1:
            if yu == 1:
                result = zh_n2[0] + result
            elif yu == 0:
                result = zh_n[0] + result
            else:
                result = zh_n[yu] + zh_n2[0] + result
        elif i == 2:
            if result[0] == zh_n2[0]:
                result = zh_n[yu] + zh_n2[1] + zh_n[1] + result
            else:
                result = zh_n[yu] + zh_n2[1] + result
        i += 1
        n = zheng
        if zheng == 0:
            break
    return result


def randomcolor():
    color_arr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    color = ""
    for _ in range(6):
        color += color_arr[random.randint(0, 14)]
    return "#" + color


def chinese_num():
    one = True
    for bai in ['', '一百', '二百', '三百', '四百', '五百', '六百', '七百', '八百', '九百']:
        for shi in ['', '一十', '二十', '三十', '四十', '五十', '六十', '七十', '八十', '九十']:
            if bai == '' and shi == '一十':
                shi = '十'
            elif bai != '' and shi == '':
                shi = '零'
            for ge in ['', '一', '二', '三', '四', '五', '六', '七', '八', '九']:
                if one:
                    one = False
                    continue
                if ge == '' and shi == '零':
                    yield bai
                else:
                    yield bai + shi + ge


def order_title(numbers, retry=False):
    for n, (a, b) in enumerate(zip(chinese_num(), numbers), 0):
        if a != b:
            if retry:
                return False
            return order_title(numbers[n:], retry=True)
        else:
            retry = False
    return True
	

# -------------好用算法----------------------
def read_csv(filepath_or_buffer, line_num, sep=",", header=True, encoding='utf-8'):
    """读取内容中有回车的csv文件"""
    with open(filepath_or_buffer, 'r', encoding=encoding) as f:
        data = f.read()
    table, line = [], []
    cells = data.split(sep)
    for n, cell in enumerate(cells):
        if len(line) == line_num - 1:
            if n == len(cells) - 1:  # 最后一个元素，允许没有\n
                line.append(cell)
                table.append(line)
                line = []
            else:
                key = cell.rfind("\n")
                if key != -1:
                    line.append(cell[:key])
                    table.append(line)
                    line = [cell[key + 1:]]
                else:
                    raise Exception("无法正确的解析表格！")
        else:
            line.append(cell)
    if header:
        return pd.DataFrame(table[1:], columns=table[0])
    else:
        return pd.DataFrame(table)


def deal_excel(df):
    """excel表读入后去除所有文本内容的首尾空格"""
    columns = [column for column in df.columns if isinstance(column, str)]
    print(columns)
    df = df.rename(columns=dict(map(lambda x: (x, x.strip()), df.columns)))
    for column in columns:
        df[column] = df[column].apply(lambda x: x.strip() if isinstance(x, str) else x)
    return df


def get_equal_rate_1(str1, str2):
    # 判断相似度的方法，用到了difflib库
    return difflib.SequenceMatcher(None, str1, str2).quick_ratio()


# -------------常用的生成器----------------------
def run_time(func):
    def wapper(*args, **kwargs):
        begin_time = time.time()
        res = func(*args, **kwargs)
        print("函数 %s 运行时间为：%.4f" % (func.__name__, time.time()-begin_time))
        return res
    return wapper

# -------------pandas操作----------------------	
# 二层遍历
df = pd.DataFrame()
df[:-1].apply(lambda x: df[x.name + 1:].apply(lambda y: deal_x(y, x), axis=1), axis=1)


if __name__ == '__main__':
    print(join_url('http://baidu.com', 'aaa'))
    print(join_url('http://baidu.com', '/aaa'))
    print(join_url('http://baidu.com/', 'aaa'))
    print(join_url('http://baidu.com/', '/aaa'))
    print('-------------------')
    print(href2url('aaa', 'http://baidu.com/'))
    print(href2url('/aaa', 'http://baidu.com/'))
    print(href2url('aaa', 'http://baidu.com'))
    print(href2url('/aaa', 'http://baidu.com'))
    print(href2url('http://baidu.com/aaa', 'http://baidu.com'))
    print(href2url('./aaa', 'http://baidu.com/'))
    print(href2url('../aaa', 'http://baidu.com/'))
    print(href2url('../../aaa', 'http://baidu.com/'))
