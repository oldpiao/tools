# 审计问题分词并合成出新词
# 思路：
# + 一般方法分词
# + 使用词性正则将一些词合并（目前词性正则貌似仍然存在一些问题）
import os

import pandas as pd

from split_words import settings
import smoothnlp
from smoothnlp import kg
from split_words.control.splitword_flow7 import splitword_flow

audit_question_file = os.path.join(settings.ROOT_DIR_P, "business/data/规则放宽的审计问题结构化.csv")
df = pd.read_csv(audit_question_file, header=0, sep='\t')
print(df.columns)

for i in df.index:
    print(df.loc[i]['规则放宽的审计问题'])
    sentence = df.loc[i]['规则放宽的审计问题']
    sentence = smoothnlp.split2sentences(sentence)
    # sentence = '你们看中华人民共和国国旗随风飘扬在天上非常美丽s壮观'
    # sentence = '一是在已开工建设的28个绿地项目中，有17个项目无基本建设程序规定的项目建议书、可行性研究报告、初步设计等批复文件'
    # print(splitword_flow(sentence).word2list2())
    # rels = kg.extract(text=sentence, pretty=True)
    # rels = smoothnlp.segment(text=sentence)
    for i in sentence:
        print([i])
        # rels = smoothnlp.ner(i)
        # print(rels)
    # for i in rels:
    #     print(i)
    # print([words.select_words(re_flag=r'^myn$').word2str()])
    # s_words = words.select_words(re_flag=r'^mynot')
    # print(len(s_words.words), s_words.word2str())
    exit()
