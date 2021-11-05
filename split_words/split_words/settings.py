import os
# 在这import jieba是为了统一接口，不需要在内部修改代码
# from split_words.my_lib.sk_log import Logger
from split_words.my_lib.my_log import Log

ROOT_DIR_P = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # 项目根目录
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # 模块根目录

logger = Log()
# logger = Logger(logname=os.path.join(ROOT_DIR, 'log.txt'), loglevel=1, logger="fox").getlog()
# logger = Logger2(loglevel=1, logger="fox").getlog()

ALL_DICT_DIR = os.path.join(ROOT_DIR, "all_dict")
RE_DICT_DIR = os.path.join(ALL_DICT_DIR, "re_dict")  # 正则分词，效果并不好，设计缺陷
SPETIAL_DICT_DIR = os.path.join(ALL_DICT_DIR, "spetial_dict")  # 特殊符号包裹的词，作为一个词，如法律法规
STOP_DICT_DIR = os.path.join(ALL_DICT_DIR, "stop_dict")  # 停用词
TAG_RE_DICT_DIR = os.path.join(ALL_DICT_DIR, "tag_re_dict")  # 词性正则的规则库
USE_DICT_DIR = os.path.join(ALL_DICT_DIR, "use_dict")

RE_DICT = os.path.join(RE_DICT_DIR, 'test.txt')
TAG_RE_DICT = os.path.join(TAG_RE_DICT_DIR, '新违规词典732_词性.txt')
# TAG_RE_DICT = os.path.join(TAG_RE_DICT_DIR, '词义词性分词规则词典.txt')
USE_DICT = os.path.join(USE_DICT_DIR, '新违规词典732_词性.txt')  # 用户添加的分词词库
USE_DICT2 = os.path.join(USE_DICT_DIR, 'computer.dic')  # 用户添加的分词词库
# USE_DICT = os.path.join(USE_DICT_DIR, 'test.txt')  # 用户添加的分词词库
SPETIAL_DICT = os.path.join(SPETIAL_DICT_DIR, '特殊符号处理.txt')  # 特殊符号内内容当一个词（会保留特殊符号）

STOP_DICT1 = os.path.join(STOP_DICT_DIR, '中文停用词库.txt')  # 停用词库
STOP_DICT2 = os.path.join(STOP_DICT_DIR, '哈工大停用词表.txt')  # 停用词库
STOP_DICT3 = os.path.join(STOP_DICT_DIR, '四川大学机器智能实验室停用词库.txt')  # 停用词库
STOP_DICT4 = os.path.join(STOP_DICT_DIR, '百度停用词列表.txt')  # 停用词库
