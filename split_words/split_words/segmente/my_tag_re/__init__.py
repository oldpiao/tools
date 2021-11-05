# 词性正则和正则分词模块
# 正则分词实际使用的不多，后面可以尝试开发其更多可能性
import re

from split_words.segmente.base import RuleBase
from split_words.segmente.my_tag_re.rule import SplitRules, cut_rule

re_my_tag_re = re.compile(r'^(.+?)( [0-9]+)?( [a-zA-Z@]+)?$', re.U)  # 词性正则配词，新增词性中允许使用@用于处理有前缀的词性


__all__ = ['MyTagRe', 'cut_rule']  # cut_rule,在words.py中有一个小功能用到了该方法纯属巧合


class MyTagRe(RuleBase):
    """ 词性正则模块
    通过词义和词性分词，可以用类似正则的格式设计
    """

    def __init__(self, default_tag='x'):
        super(MyTagRe, self).__init__(re_suledict=re_my_tag_re, default_tag=default_tag)
        # 默认词性为x,这会导致分词规则未加词性又仅仅匹配到一个词时，该词的词性被修改为x
        # 可以设计相关算法，或使用jieba库中的功能联想该词词性，需要付出一定的计算资源

    def add_word(self, word, freq=None, tag=None):
        if word not in self.rules:
            self.rules[word] = SplitRules(word, freq, tag)
            # self.rules[word] = {'split_rule': self.str2list(word), 'freq': freq, 'tag': tag}

    def cut(self, words):
        """
        :param words: list 格式: [MyPair(), MyPair(),...], 其中MyPair为: from split_words.utils import MyPair
        :return:
        """
        i = 0
        new_words = []
        len_words = len(words)
        while i < len_words:
            old_i = i
            for rule, split_rule in self.rules.items():
                new_word, ln = split_rule.match(words[i:])
                if new_word is not None:
                    # 退出时new_word中有数据,证明匹配到了内容，则从匹配到的内容结尾继续开始
                    i = ln + i
                    new_words.append(self.new_word(new_word[0], new_word[1], end_word_flag=new_word[2]))
                    break

            if i == old_i:
                new_words.append(words[i])  # 未匹配到时，记录一个词
                i += 1  # 并前进一个词继续匹配
        return new_words
