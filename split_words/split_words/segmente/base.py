# 分词后对分词结果进行处理的模块的基础类
import collections  # 有序字典

from split_words.my_lib import func
from split_words.segmente import utils
from split_words.utils import MyPair


class DealBase(object):
    """处理模块基础类, 记录对模块本身参数的处理，对词典的增删改查
    具体功能有些需要在子类中实现，在此类似于声明的作用
    这里并未指定存储数据的词典的名字，方便子类指定
    """
    def add_word(self, word, freq=None, tag=None):
        pass

    def add_words(self, words):
        pass

    def load_dict(self, filepath):
        """文本要求是utf8编码，一行为一个词"""
        words = [line for lineno, line in func.openfile(filepath)]
        self.add_words(words)

    def del_word(self, word):
        pass

    def del_words(self, words):
        for word in words:
            self.del_word(word)


class SetBase(DealBase):
    """处理模块添加文本格式词典
    除了词外没有任何其他信息
    """
    def __init__(self, words=None):
        """
        :param words: set() 必须是set型的，后续的会用到set的一些方法
        """
        self.words = words or set()

    def add_word(self, word, freq=None, tag=None):
        self.words.add(word)

    def add_words(self, words):
        self.words.update(words)

    def load_dict(self, filepath):
        """文本要求是utf8编码，一行为一个词"""
        words = [line.strip() for lineno, line in func.openfile(filepath)]
        self.add_words(words)

    def del_word(self, word):
        if word in self.words:
            self.words.remove(word)

    def del_words(self, words):
        self.words = self.words.difference(words)


class RuleBase(DealBase):
    """正则模块基础模块"""
    def __init__(self, re_suledict, default_tag='x'):
        """
        :param re_suledict: 词典获取规则，实际是一个正则
        rules: 有向字典，格式为 "规则": {"freq": 词频, "tag": 词性}
        """
        self.default_tag = default_tag
        self.re_suledict = re_suledict
        self.rules = collections.OrderedDict()

    def get_tag(self, tag, end_word_flag):
        return utils.get_tag(tag=tag, default_tag=self.default_tag, end_word_flag=end_word_flag)

    def new_word(self, word, tag=None, end_word_flag='x'):
        return MyPair(word, flag=self.get_tag(tag=tag, end_word_flag=end_word_flag))

    def add_word(self, word, freq=None, tag=None):
        if word not in self.rules:
            self.rules[word] = {'freq': freq, 'tag': tag}

    def load_dict(self, filepath):
        for lineno, line in func.openfile(filepath):
            word, freq, tag = self.re_suledict.match(line).groups()
            if freq is not None:
                freq = freq.strip()
            if tag is not None:
                tag = tag.strip()
            self.add_word(word, freq, tag)

    def del_word(self, word):
        if word in self.rules.keys():
            self.rules.pop(word)
