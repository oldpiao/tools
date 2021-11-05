# 结果集处理模块，分词结果放在此
# 将分词结果作为一个类存储，可以在其中实现一些对分词结果的处理功能
# 该页中的词要么是原来的词，要么即使是新词也不存在修改词性的问题，因此直接使用MyPair创建
import re
from split_words.utils import MyPair

# from split_words.segmente.my_tag_re import cut_rule

__all__ = ['Words', 'POSWords']


# 匹配当前字符是否为特殊字符，用于分割句子
# 空格也作为分割符传进去了
re_symbol = re.compile(r'^[。.,，？?!！；;:：（(）)\r\n\t ]$', re.U)


class WordsBase(object):
    def __init__(self, words):
        self.words = list(words)

    def _2str(self, word):
        return word

    def _2list(self, word):
        # {'word': word.word, 'flag': word.flag}
        return word

    def word2str(self):
        words = ''
        for word in self.words:
            words += self._2str(word)
        # logger.info('word2str: %s' % words[:-1])
        return words[:-1]

    def word2list(self):
        words = []
        for word in self.words:
            words.append(self._2list(word))
        return words


class Words(WordsBase):
    """不词性的词的集合，以及一些处理方法， 实际用到的情况不多"""
    def __init__(self, words):
        """将生成器对象的words转为list格式"""
        super(Words, self).__init__(words)

    def _2str(self, word):
        return word + '/'


class POSWords(WordsBase):
    """带词性的词的集合，以及一些处理方法"""
    def __init__(self, words):
        """将生成器对象的words转为list格式"""
        super(POSWords, self).__init__(words)

    # @classmethod
    # def str2words_old(cls, sentence):
    #     """
    #     将"审计/v/结果表明/n/"这种格式的内容转换成POSWords对象
    #     目前存在无法处理转义的/的问题，会被当成单词分隔符使用
    #     """
    #     word_list = []
    #     for word_or_flag in sentence.split('///'):
    #         word_list.extend(word_or_flag.split('/'))
    #         word_list.append('/')
    #     word_list = word_list[:-1]
    #     words = []
    #     for word, flag in zip(word_list[::2], word_list[1::2]):
    #         words.append(MyPair(word, flag))
    #     return cls(words)

    # @classmethod
    # def str2words(cls, sentence):
    #     """ 一个意义不大的小功能，可以将转出的字符串转回成实例化对象
    #     将"审计/v/结果表明/n/"这种格式的内容转换成POSWords对象
    #     目前可以处理转义的/的问题，使用转义字符转义后不会被当成单词分隔符使用
    #     但遇到同义词转化的情况就会出问题，要么是丢失原文本信息，要么是读取错误
    #     因此不建议使用
    #     """
    #     word_list = list(cut_rule(sentence))
    #     # print(word_list)
    #     words = []
    #     for word, flag in zip(word_list[::2], word_list[1::2]):
    #         words.append(MyPair(word, flag))
    #     return cls(words)

    def deal_words(self, obj):
        self.words = obj(self.words)
        return self

    def _2str(self, word):
        return word.word + '/' + word.flag + '/'

    def _2str2(self, word, separator='/'):
        return word.word + separator

    def _2list(self, word):
        return {'word': word.word, 'flag': word.flag}

    def _2list2(self, word):
        return word.word

    def word2str2(self, separator='/'):
        """不要词性"""
        words = ''
        for word in self.words:
            words += self._2str2(word, separator)
        # logger.info('word2str2: %s' % words[:-1])
        return words[:-1]

    def word2list2(self):
        """不要词性"""
        words = []
        for word in self.words:
            words.append(self._2list2(word))
        return words

    def judge1(self, flag, re_flag):
        """使用正则过滤词性"""
        if re_flag is None:
            return True
        else:
            return re.search(re_flag, flag) is not None

    def judge2(self, word, min_len=None):
        """过滤长度小于最小长度的"""
        if min_len is None:
            return True
        else:
            return len(word) >= min_len

    def judge3(self, flag, ignore):
        """词性在ignore中的不要"""
        if ignore is None:
            return True
        else:
            return flag not in ignore

    def judge4(self, word, my_filter):
        if my_filter is None:
            return True
        else:
            return my_filter(word)

    def judge5(self, word, my_judge):
        """or规则,因此默认为Flase"""
        if my_judge is None:
            return False
        else:
            return my_judge(word)

    def select_words(self, re_flag=None, min_len=None, ignore=None, my_filter=None, my_judge=None):
        """根据flag获取部分词
        :param re_flag: str正则的判断规则，用于代替原本的flags参数，改为正则可以更灵活的判断
        :param min_len: int word长度小于等于该值的不要
        :param ignore:  list 词性在该列表中的不要
        :param my_filter:  object 自定义的筛选规则，参数为word返回结果为True or False，与其他规则一起使用
        :param my_judge:  object 自定义的判断规则，参数为word返回结果为True or False，独立于其他规则使用
        :return: POSWords  筛选后的结果组成一个分词类返回
        """
        words = []
        for word in self.words:
            if self.judge1(word.flag, re_flag) and self.judge2(word.word, min_len) \
                    and self.judge3(word.flag, ignore) and self.judge4(word, my_filter) \
                    or self.judge5(word, my_judge):
                # words += word.word + ' '
                words.append(word)
        return POSWords(words=words)

    def de_weight(self):
        """数据去重
        :return: 返回一个新的POSWords实例对象
        """
        words = list(set(self.words))
        return POSWords(words=words)

    def deal_word(self, deal_way):
        """数据的二次处理, 加入过滤功能，当词处理后变成不符合规定的词时，返回None可以删除该词
        :param deal_way:  object 自定义的结果处理规则，对于分词不理想的词进行拆分，但不会影响原分词结果
                            参数为word.word返回结果为word.word
        :return: 返回一个新的POSWords实例对象
        """
        words = []
        for word in self.words:
            new_word_word = deal_way(word)
            if new_word_word is None:
                pass
            else:
                words.append(MyPair(new_word_word, word.flag))
        return POSWords(words=words)

    def to_sentences(self, flag='xs'):
        """以句为单位将原文本中的分词合并成一句，词中间用空格隔开"""
        sentences = []
        sentence, new_flag = '', None
        for word in self.words:
            if sentence_end(word):
                if sentence != '':
                    sentences.append(MyPair(sentence[:-1], flag=new_flag))
                sentence, new_flag = '', None
            else:
                sentence += self._2str2(word, separator=' ')  # 空格隔开
                if new_flag is None:
                    new_flag = word.flag
                elif new_flag != word.flag:
                    new_flag = flag
                else:
                    pass
        return POSWords(words=sentences)


def sentence_end(word):
    """保留每一句话中的逗号句号(小数点为词性为m的句号，因此需要判断一下词性)，
    暂时无法解决100,000,000这样的问题，建议提前将其分词
    """
    if re_symbol.search(word.word) is not None and word.flag == 'x':
        return True
    else:
        return False


if __name__ == '__main__':
    # ss = SpetialSigns()
    # filepath = 'D:/job/审计公告/审计问题分词/split_words/all_dict/spetial_dict/特殊符号处理.txt'
    # ss.load_dict(filepath)
    print(sentence_end(MyPair('\n', 'x')))
    # all_word = POSWords.str2words(r"管理不规范/dj@nn/问题\/金额/sc@n/11.1/m/亿元/m/，")
    # print(all_word.word2list())
