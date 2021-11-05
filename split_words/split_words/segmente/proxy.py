# 分词后对分词结果进行处理的模块
# deal_words统一接口，处理[MyPair, MyPair, ...]
# deal_words2统一接口，处理[word, word, ...]
from collections import Counter
import re

from split_words.my_lib import func
from split_words.segmente import utils
from split_words.segmente.base import SetBase, RuleBase

# 新增词性可以匹配大写字母，因为其他模块存在使用大写字母表示的词性
# 新增允许匹配@因为打算把@加入词性中切分前缀
re_spetial_signs = re.compile(r'^(.+?) (.+?)( [0-9]+)?( [a-zA-Z@]+)?$', re.U)  # 特殊符号处理模块

__all__ = ['StopWords', 'ReStopWords', 'SpetialSigns', 'Loaners', 'ReLoaners', 'AllLoaners', 'SightWords']


class StopWords(SetBase):
    """停用词"""

    def del_stop_words(self, words):
        """去除停用词"""
        for word in words:
            if word.word not in self.words:
                yield word

    def deal_words(self, words):
        """统一接口"""
        return self.del_stop_words(words)

    def del_stop_words2(self, words):
        """去除停用词"""
        for word in words:
            if word not in self.words:
                yield word

    def deal_words2(self, words):
        """统一接口"""
        return self.del_stop_words2(words)


class ReStopWords(SetBase):
    """正则停用词"""

    def del_re_stop_words(self, words, *args, **kwargs):
        """去除停用词"""
        for word in words:
            is_stop_words = False
            for rule in self.words:
                if re.search(rule, word.word, *args, **kwargs) is not None:
                    is_stop_words = True
                    break
            if not is_stop_words:
                yield word

    def deal_words(self, words, *args, **kwargs):
        """统一接口"""
        return self.del_re_stop_words(words, *args, **kwargs)

    def del_re_stop_words2(self, words, *args, **kwargs):
        """去除停用词"""
        for word in words:
            is_stop_words = False
            for rule in self.words:
                if re.search(rule, word, *args, **kwargs) is not None:
                    is_stop_words = True
                    break
            if not is_stop_words:
                yield word

    def deal_words2(self, words, *args, **kwargs):
        """统一接口"""
        return self.del_re_stop_words2(words, *args, **kwargs)


class SpetialSigns(RuleBase):
    """特殊符号处理，将特殊符号中的词当成一个词"""
    def __init__(self, default_tag='x'):
        super(SpetialSigns, self).__init__(re_suledict=re_spetial_signs, default_tag=default_tag)

    def load_dict(self, filepath):
        for lineno, line in func.openfile(filepath):
            begin, end, freq, tag = self.re_suledict.match(line).groups()
            if freq is not None:
                freq = freq.strip()
            if tag is not None:
                tag = tag.strip()
            self.add_word((begin, end), freq, tag)

    def add_word(self, word, freq=None, tag=None):
        if word[0] not in self.rules:
            self.rules[word[0]] = {'end': word[1], 'freq': freq, 'tag': tag}

    def _deal_spetialsigns(self, words, i=0, new_words=None):
        """ 针对带词性的情况做的,适用于Words类
        :param words: list, [MyPair, MyPair, ...]
        :param i: 当前处理到了哪个词了
        :param new_words: 最终的处理结果, 递归算法，因此跟随程序
        :return: new_words: list, [MyPair, MyPair, ...]
        """
        if new_words is None:
            new_words = []
        new_word, info, new_begin = '', None, None
        while i < len(words):
            if info is not None:
                # 找到结尾，将其提成一个词
                new_word += words[i].word
                if words[i].word == info['end']:
                    new_words.append(self.new_word(new_word, info['tag'], words[i].flag))
                    info, new_word = None, ''
            elif words[i].word in self.rules.keys():
                info = self.rules[words[i].word]
                new_word, new_begin = words[i].word, i
            else:
                new_words.append(words[i])
            i += 1
        if new_word != '':
            if info is not None:  # 此时，begin一定时被重新赋过值的
                # 未找到结束标识，记录当前字符，重新循环
                new_words.append(words[new_begin])
                return self._deal_spetialsigns(words, new_begin + 1, new_words)
            else:  # 该情况发生，证明循环在第二步退出，即发现一个特殊符号，但已是最后一个字符
                new_words.append(words[-1])
        return new_words

    def deal_spetialsigns(self, words):
        for word in self._deal_spetialsigns(words):
            yield word

    def deal_words(self, words):
        """统一接口"""
        return self.deal_spetialsigns(words)

    def deal_spetialsigns2(self, words):
        """ 针对无词性的情况做的,适用于Words类
        :param words: list, [str, str, ...]
        :return: words: list, [str, str, ...]
        """
        # for word in self.words:
        i = 0
        while i < len(words):
            if words[i] in self.rules.keys():
                info = self.rules[words[i]]
                try:
                    find_end = words[i + 1:].index(info['end']) + i + 1
                    yield ''.join(words[i:find_end + 1])
                    i = find_end
                except:
                    yield words[i]
            else:
                yield words[i]
            i += 1


class LoanersBase(object):

    def __init__(self):
        self.loaner2weight = {}

    def search(self, word):
        """查询单词是否在词典中，如果不在返回None
        :param word: word.word，目前是不包含词性的
        """
        return None

    def replace(self, words):
        """替换为同义词, 包括正则匹配相同和同义词库
        :param words: list, [MyPair, ...]
        :return: words
        """
        for word in words:
            loaner = self.search(word.word)
            if loaner is not None:
                word.set_raw_word(loaner)
            yield word

    def deal_words(self, words):
        """统一接口"""
        return self.replace(words)

    def replace2(self, words):
        """替换为同义词, 包括正则匹配相同和同义词库
        :param words: list, [word, ...]
        :return: words
        """
        for word in words:
            loaner = self.search(word)
            if loaner is not None:
                word.set_raw_word(loaner)
            yield word

    def deal_words2(self, words):
        """统一接口"""
        return self.replace2(words)

    def get_weight(self, loaner):
        """
        获取当前词的权重，设置为同义词后导致一些词合并，因此设置了一个权重项，
        目前使用时并未用到
        """
        if loaner not in self.loaner2weight.keys():
            return None
        return self.loaner2weight[loaner]


class Loaners(LoanersBase):
    """
    同义词模块
    同义词的代替词集合与其在原文中的权重
    """
    def __init__(self):
        super(Loaners, self).__init__()
        self.word2loaner = dict()  # {word1: key, word2: key1, word3: key2}  # 同义词词典

    def add(self, key, words, weight=0):
        for word in words:
            self.word2loaner[word] = key
        self.loaner2weight[key] = weight

    def load_dict(self, thesaurus_txt, weight=2):
        all_words = utils.get_thesaurus(thesaurus_txt)
        for words in all_words:
            self.add(words[0], words[1:], weight=weight)

    def search(self, word):
        """查询是否为手工添加的词典中的同义词"""
        if word not in self.word2loaner.keys():
            return None
        return self.word2loaner[word]

    def get_weight(self, loaner):
        """
        获取当前词的权重，设置为同义词后导致一些词合并，因此设置了一个权重项，
        目前使用时并未用到
        """
        if loaner not in self.loaner2weight.keys():
            return None
        return self.loaner2weight[loaner]


class ReLoaners(LoanersBase):
    """
    正则同义词模块，正则格式的方式匹配实际并不算是同义词
    """
    def __init__(self):
        super(ReLoaners, self).__init__()
        self.word2loaner = []  # [(key, re_compile)]  # 正则同义词词典，有序

    def add_all(self):
        self.add_privative()
        self.add_num()
        return self

    def add(self, key, re_rule, weight=0):
        self.word2loaner.append((key, re_rule))
        self.loaner2weight[key] = weight

    def add_privative(self, key="<否定词>", weight=1):
        """添加正则规则-否定词"""
        re_privative = re.compile(r'^不|^未[^来]')
        self.add(key, re_privative, weight)

    def add_num(self, key="<数词>", weight=0):
        """添加正则规则-数词"""
        re_num = re.compile(r'^\d+\.?\d*$')
        self.add(key, re_num, weight)

    def search(self, word):
        """查询是否为默认的同义词"""
        for key, rule in self.word2loaner:
            if rule.search(word) is not None:
                return key
        return None


class AllLoaners(LoanersBase):
    """
    同义词模块
    同义词的代替词集合与其在原文中的权重
    以及正则格式的同义词，正则格式的方式匹配实际并不算是同义词，但操作相同，且意义相似，就放在了一块
    """

    def __init__(self, loaners=None, re_loaners=None):
        """
        :param loaners: 同义词词典
        :param re_loaners: 正则格式同义词词典
        """
        super(AllLoaners, self).__init__()
        self.loaners = loaners or Loaners()
        self.re_loaners = re_loaners or ReLoaners().add_all()

    def search(self, word):
        """两种方法都使用的查询方法"""
        result = self.loaners.search(word)
        if result is None:
            result = self.re_loaners.search(word)
        return result

    def get_weight(self, loaner):
        """
        获取当前词的权重，设置为同义词后导致一些词合并，因此设置了一个权重项，
        目前使用时并未用到
        """
        if loaner in self.loaners.loaner2weight.keys():
            return self.loaners.loaner2weight[loaner]
        elif loaner in self.re_loaners.loaner2weight.keys():
            return self.re_loaners.loaner2weight[loaner]
        return None


class SightWords(object):
    """高频词筛选
    一般用于通过控制词的数量控制词向量的长度
    """

    def __init__(self, words=None):
        self.sight_words = words or {}

    @classmethod
    def keep_eq_freq(cls, word_freqs: Counter, n):
        """保留与最后一个词词频相同的词"""
        words = word_freqs.most_common()
        # print(words[n-1: n+1])
        if n >= len(words):
            return dict(words)
        sight_words = dict(words[:n])
        n_freq = words[n-1][1]
        for word, freq in words[n:]:
            if freq == n_freq:
                sight_words[word] = freq
            else:
                break
        return cls(sight_words)

    @classmethod
    def top_n(cls, words: list, n=100, keep_freq=False):
        """
        保留词频排行前n的词
        :param words: 此处的words与其他模块不同采用的是
        :param n: top_n个词
        :param keep_freq: 是否保留与最后一个词频率相同的词
        :return:
        """
        # 如有需要，后期可以换成有向词典
        word_freqs = Counter(words)
        if keep_freq:
            return cls.keep_eq_freq(word_freqs, n)
        return cls(dict(word_freqs.most_common(n)))

    @classmethod
    def top_percent(cls, words: list, percent=0.1, keep_freq=False):
        """词频最高的N%的词"""
        word_freqs = Counter(words)
        n = int(len(word_freqs.keys()) * percent)
        if keep_freq:
            return cls.keep_eq_freq(word_freqs, n)
        return cls(dict(word_freqs.most_common(n)))

    @classmethod
    def freq_gt_n(cls, words, n=2):
        """词频大于n的所有的词"""
        word_freqs = Counter(words)
        sight_words = {}
        for word, freq in word_freqs.most_common():
            if freq > n:
                sight_words[word] = freq
            else:
                break
        return cls(sight_words)

    def del_low_freq_words(self, words):
        """删除低频词"""
        for word in words:
            if word.word in self.sight_words:
                yield word

    def deal_words(self, words):
        """统一接口"""
        return self.del_low_freq_words(words)

    def del_low_freq_words2(self, words):
        """删除低频词"""
        for word in words:
            if word in self.sight_words:
                yield word

    def deal_words2(self, words):
        """统一接口"""
        return self.del_low_freq_words2(words)


# if __name__ == '__main__':
#     words = list('aaaabbbcccdddeerrffjjlkpi')
#     all_word = SightWords.top_n(words, n=2, keep_freq=True)
#     print(all_word.words)
#     all_word = SightWords.top_percent(words, percent=0.2, keep_freq=True)
#     print(all_word.words)
#     all_word = SightWords.freq_gt_n(words, n=2)
#     print(all_word.words)
