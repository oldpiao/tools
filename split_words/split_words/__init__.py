import re
from jieba import posseg

from split_words.utils import MyPair
from split_words.words import POSWords  # 结果集类型
from split_words.segmente import RuleBase
# from split_words.segmente import *  # 更多处理规则
# from split_words.cut_text import *  # 切分句子的工具集

# 正则配词虽然在结巴分词前，但仍能有特殊符号
re_my_re = re.compile(r'^(.+?)( [0-9]+)?( [a-zA-Z@]+)?$', re.U)  # 正则配词


name = '分词模块'
version = '2.3.2'


class MyPOSTokenizer(posseg.POSTokenizer):
    """自定义分词模块"""

    def load_userdict(self, filepath):
        self.tokenizer.load_userdict(filepath)

    def cut(self, sentence, HMM=True):
        for w in super(MyPOSTokenizer, self).cut(sentence, HMM=HMM):
            yield MyPair.init(w)

    def pws_cut(self, *args, **kwargs):
        """将结果以list格式返回，放在这怕忘了，实际不用重写"""
        return POSWords(words=self.lcut(*args, **kwargs))

    @property
    def user_word_tag_tab(self):
        """获取用户词典"""
        return self.tokenizer.user_word_tag_tab


class RePOSTokenizer(RuleBase):
    """正则分词模块
    正则模块依次使用正则规则匹配词，将匹配到的词作为单独的词存储并将匹配到的词前后的词也进行相同操作，
    对于未能匹配到的部分使用正常的分词处理，由于使用了递归可能会面临递归超出限制的情况，应该注意该问题，
    建议使用该模块前先将文章分句，再处理。
    """
    def __init__(self, tokenizer=None, default_tag='x'):
        """
        :param tokenizer: MyPOSTokenizer
        :param default_tag: 默认标签，在正则分词模块中不建议在任何位置使用自动标签，如果使用会设置为x
        """
        super(RePOSTokenizer, self).__init__(re_suledict=re_my_re, default_tag=default_tag)
        self.tokenizer = tokenizer or MyPOSTokenizer()

    @property
    def jieba(self):
        """Tokenizer()该模块使用的分词实例化
        这样写是为了与结巴直接调用时看起来类似
        """
        return self.tokenizer.tokenizer

    @property
    def posseg(self):
        """POSTokenizer()该模块使用的带词性的分词的实例化
        这样写是为了与结巴直接调用时看起来类似
        """
        return self.tokenizer

    def dt_load_userdict(self, filepath):
        """结巴分词添加词典"""
        self.tokenizer.load_userdict(filepath)

    def get_dt_userdict(self):
        """获取结巴用户词典"""
        return self.tokenizer.user_word_tag_tab

    def _cut(self, sentence, rules: dict, *args, **kwargs):
        """递归查词"""
        status = False
        for rule, v in rules.items():
            result = re.search(rule, sentence, *args, **kwargs)
            if result is not None:
                new_rules = rules.copy()
                new_rules.pop(rule)
                # 前面的不需要再用当前规则
                for word in self._cut(sentence[:result.start()], new_rules, *args, **kwargs):
                    yield word
                # 由于标签有可能是自动标签，因此此处将正则匹配结果做了分词，取最后一个的词性
                # 这样做增加了计算量，但丰富了功能，存在优化空间
                yield self.new_word(
                    result.group(), v['tag'],
                    end_word_flag=self.tokenizer.lcut(result.group())[-1].flag
                )
                for word in self._cut(sentence[result.end():], rules, *args, **kwargs):
                    yield word
                status = True
                break
                # return results, v['freq'], v['tag']
        if not status:
            for word in self.tokenizer.cut(sentence):
                yield word

    def cut(self, sentence, *args, **kwargs):
        """分词模块"""
        return self._cut(sentence, self.rules, *args, **kwargs)

    def lcut(self, *args, **kwargs):
        """list格式words"""
        return list(self.cut(*args, **kwargs))

    def pws_cut(self, *args, **kwargs):
        """将结果以list格式返回，放在这怕忘了，实际不用重写"""
        return POSWords(words=self.lcut(*args, **kwargs))
