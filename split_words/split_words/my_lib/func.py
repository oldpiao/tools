import time
import math

from pandas import DataFrame
from split_words.settings import logger


string_types = (str,)
text_type = str


def run_time(func):
    def wapper(*args, **kwargs):
        begin_time = time.time()
        res = func(*args, **kwargs)
        logger.info("函数 %s 运行时间为：%.4f" % (func.__name__, time.time()-begin_time))
        return res
    return wapper


def strdecode(sentence):
    if not isinstance(sentence, text_type):
        try:
            sentence = sentence.decode('utf-8')
        except UnicodeDecodeError:
            sentence = sentence.decode('gbk', 'ignore')
    return sentence


def resolve_filename(f):
    try:
        return f.name
    except AttributeError:
        return repr(f)


def openfile(f):
    if isinstance(f, string_types):
        f_name = f
        f = open(f, 'rb')
    else:
        f_name = resolve_filename(f)
    for lineno, ln in enumerate(f, 1):
        line = ln.strip()
        if not isinstance(line, text_type):
            try:
                line = line.decode('utf-8').lstrip('\ufeff')
            except UnicodeDecodeError:
                raise ValueError('dictionary file %s must be utf-8' % f_name)
        if not line:
            continue
        yield lineno, line


@run_time
def get_word_infos(all_words):
    """计算段落结构字段分词后的词频，计算tfidf值"""
    # 并非所有模块都需要
    from gensim import corpora
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
        words.append([word, cfs, dfs, tf, idf, tf_idf])

    columns = ['word', '全文词数', '有该词的句数', '词频', '逆文本频率', 'tf_idf']
    return DataFrame(words, columns=columns)
