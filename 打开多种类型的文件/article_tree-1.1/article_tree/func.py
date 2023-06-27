# -*- coding:utf-8 -*-
import os
import shutil
import time
import json
import re
import difflib
import logging


class MyJSON2(object):
    """以行字符串的形式逐行存储，以json格式逐行读取"""
    def __init__(self, f_path):
        self.f_path = f_path

    def addline(self, data):
        """未经处理的列表"""
        self.addline_str(json.dumps(data, ensure_ascii=False))

    def addline_str(self, data):
        """已处理成json格式的"""
        with open(self.f_path, "a", encoding='utf-8') as f:
            f.write(data)
            f.write('\n')

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


def get_files(file_dir, second=''):
    """轮训获取路径下的所有文件，会自动查询进一步的路径并返回拼接后的相对路径文件名"""
    for f in os.listdir(file_dir):
        if os.path.isdir(os.path.join(file_dir, f)):
            for i in get_files(os.path.join(file_dir, f), os.path.join(second, f)):
                yield i
        else:
            yield os.path.join(second, f)


def rep_spetial_char(fname, rep='_'):
    """将文件名中的特殊字符替换为指定字符"""
    return re.sub(r'[\\/:*?"<>|\n\t\r]', rep, fname)


def run_time(func):
    def wapper(*args, **kwargs):
        begin_time = time.time()
        res = func(*args, **kwargs)
        logging.info("函数 %s 运行时间为：%.4f" % (func.__name__, time.time()-begin_time))
        return res
    return wapper


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


def read_file(fpath):
    """获取文本内容"""
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    return content


def get_equal_rate_1(str1, str2):
    # 判断相似度的方法，用到了difflib库
    return difflib.SequenceMatcher(None, str1, str2).quick_ratio()


def chinese_num():
    """从一开始"""
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


def chinese_num2():
    yield '零'
    for i in chinese_num():
        yield i


def verify_ch_num(chnum):
    """验证获取到的确实是当前可处理的中文数字，避免在转换时无法处理"""
    if re.search('^[零一二三四五六七八九十百]+$', chnum):
        return True
    return False


def chnum2int(chnum):
    c_nums = chinese_num2()
    i = 0
    try:
        while True:
            j = next(c_nums)
            if j == chnum:
                return i
            i += 1
    except StopIteration:
        print('%s不是一个正常的数字' % chnum)
        return None


def int2chnum(num: int):
    """数字转中文数字"""
    c_nums = chinese_num2()
    if num < 0:
        raise TypeError('num不允许为负数')
    if num == 0:
        return next(c_nums)
    for _ in range(num):
        next(c_nums)
    return next(c_nums)


def int2chnum2(num: int):
    """允许负数"""
    if num < 0:
        return '负' + int2chnum(-num)
    else:
        return int2chnum(num)


def order_nums(numbers):
    for a, b in zip(chinese_num(), numbers):
        if a != b:
            return False
    return True


# class MissNums(object):
#     def __init__(self, begin, end, miss_nums):
#         self.begin = begin
#         self.end = end
#         self.miss_nums = miss_nums


def find_miss_nums(nums, v_top=None):
    """
    :param nums:
    :param v_top: 从哪一位开始算缺失数字，默认为None，从给定的数字的开始算
    :return:
    """
    begin = nums[0]
    if v_top is not None:
        next = v_top
    else:
        next = begin
    n = 0
    miss_nums = []
    while n < len(nums):
        if nums[n] < next:
            if v_top is not None:
                next = v_top
            else:
                next = begin
            continue
        if nums[n] == next:
            n += 1
        else:
            miss_nums.append(next)
        next += 1
    return miss_nums
    # return MissNums(begin, nums[-1], miss_nums)


if __name__ == '__main__':
    print(int2chnum(0))
    print(int2chnum(10))
    print(chnum2int('零'))
    print(chnum2int('二十三'))
    print(chnum2int('十十'))
