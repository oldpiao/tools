import re

# 词性正则工具箱
AUTO_TAG = 'auto'
LEN_AUTO_TAG = len(AUTO_TAG)


def get_tag(tag, default_tag='x', end_word_flag='x'):
    """ 词性选择方法，从三种词性中选择词性作为当前词的词性
    允许使用自动配置，自动配置即选用end_word_flag
    :param tag: 词典配置的词性
    :param default_tag: 默认词性
    :param end_word_flag: 多个词组合成新词时的最后一个词的词性
    :return:
    """
    # 当前词词性为空时用默认词性代替当前词性
    if tag is None:
        return get_tag(default_tag, default_tag, end_word_flag)
    # 词典配置为自动，返回结束词词性
    elif tag == AUTO_TAG:
        return end_word_flag
    elif '@' + AUTO_TAG == tag[-LEN_AUTO_TAG-1:]:
        # 带前缀的自动词性，注意end_word_flag可能也是带前缀的词，此时会有两个前缀
        return tag[:-LEN_AUTO_TAG] + end_word_flag
    else:
        return tag


def get_thesaurus(thesaurus_txt):
    """获取同义词词典"""
    with open(thesaurus_txt, 'r', encoding='utf-8') as f:
        all_words = [re.split(r'\s+', i.strip()) for i in f.readlines()]
    return all_words
