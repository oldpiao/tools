# 分词模块工具集
import re
from jieba.posseg import pair


class ReCutSentence(object):
    """切分句子的正则"""
    def __init__(self):
        self.re_enter = re.compile(r'\n+')
        self.re_by_the_operator = re.compile(r'[^;；。?？!！]+[;；。?？!！]?')

    def split(self, string, *args, **kwargs):
        for sentence1 in self.re_enter.split(string, *args, **kwargs):
            for sentence2 in self.re_by_the_operator.findall(sentence1.strip()):
                yield sentence2


class ReClause(object):
    """切分子句的正则"""
    def __init__(self):
        self.re_clause = re.compile(r'[^:：,，]+[:：,，]?')

    def findall(self, string, *args, **kwargs):
        clauses = self.re_clause.findall(string, *args, **kwargs)
        if len(clauses) == 0:
            return ['']
        return clauses


class CutSpetialNumber(object):
    """切分出用逗号分开的数字"""

    def __init__(self, clauses):
        self.clauses = clauses

    @classmethod
    def init(cls, sentence):
        re_cut_spetial_number = re.compile(r'([0-9,，]+[,，][0-9,，]+)')
        return cls(re_cut_spetial_number.split(sentence))

    def get_spetial_number(self):
        if len(self.clauses) < 2:
            return []
        return self.clauses[1::2]

    def get_clauses(self):
        return self.clauses[::2]


class MyPair(pair):
    """同义词或原文中被用符号替代的词"""
    def __init__(self, word, flag, raw_word=None):
        super(MyPair, self).__init__(word, flag)
        self.raw_word = raw_word

    @classmethod
    def init(cls, word: pair):
        return cls(word.word, word.flag)

    def __unicode__(self):
        if self.raw_word is not None:
            return '%s/%s/%s' % (self.word, self.raw_word, self.flag)
        else:
            return super(MyPair, self).__unicode__()

    def is_replaced(self):
        return self.raw_word is not None

    def set_raw_word(self, loaner):
        """将一些词归类, 属于同义词的概念
        不XX、未XX = <否定词>
        12、23.45 = <数词>
        """
        self.raw_word = self.word
        self.word = loaner
