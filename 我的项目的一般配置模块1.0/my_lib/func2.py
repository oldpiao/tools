# 数据挖掘模块延伸出的一些方法
import math

from pandas import DataFrame
from gensim import corpora


def get_word_infos(all_words):
    """计算段落结构字段分词后的词频，计算tfidf值"""
    dictionary = corpora.Dictionary(all_words)
    # print(dictionary.token2id)
    # print(dictionary.cfs)  # 一个词出现几次
    # print(dictionary.dfs)  # 一个词出现在几句话中
    words = []
    sum_words = sum([len(words) for words in all_words])  # 总词数
    N = len(all_words)  # 总句数
    for word, id in dictionary.token2id.items():
        cfs = dictionary.cfs[id]  # 词数
        tf = cfs/sum_words  # 词频
        dfs = dictionary.dfs[id]  # 词word存在的句数
        # idf = math.log((N + 1)/(dfs + 1)) + 1  # k1平滑的idf
        idf = math.log(N/dfs)  # 一般类型的idf
        tf_idf = tf * idf
        words.append([id, word, cfs, dfs, tf, idf, tf_idf])

    columns = ['id', 'word', '全文词数', '有该词的句数', '词频', '逆文本频率', 'tf_idf']
    return DataFrame(words, columns=columns)
