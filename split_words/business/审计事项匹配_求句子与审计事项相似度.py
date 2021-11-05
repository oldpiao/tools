import os
import json
import difflib

import pandas as pd
from split_words.cut_text import cut_sentence, cut_clause

ROOT_DIR = "D:/job/审计公告/审计问题分词/split_words/business/data/审计事项匹配"
DICT_DIR = os.path.join(ROOT_DIR, "预算执行审计事项字典.xls")
DF_DICT = pd.read_excel(DICT_DIR, header=0)


def get_equal_rate_1(str1, str2):
    str1, str2 = set(str1), set(str2)
    return len(str1 & str2) / len(str2)

# def get_equal_rate_1(str1, str2):
#     result = 0
#     # 从两个字符串中找到共同的字符
#     for char in str1:
#         if char in str2:
#             result += 1
#     return result / len(str2)


# 判断相似度的方法，用到了difflib库
def get_equal_rate_2(str1, str2):
   return difflib.SequenceMatcher(None, str1, str2).quick_ratio()


def get_similarity(str1):
    max_similarity = {"similarity": 0}
    for line in DF_DICT.to_dict("records"):
        similarity = get_equal_rate_1(str1, line['二级审计事项'])
        if max_similarity["similarity"] < similarity:
            max_similarity = {"similarity": similarity}
            max_similarity.update(line)
    return max_similarity


def read_file(key, min_sim=0.5):
    file_path = os.path.join(ROOT_DIR, "预算执行审计报告和整改报告.csv")
    df = pd.read_csv(file_path, header=0, index_col=0)
    print(df.shape)
    df = df[df[key].notnull()]
    print(df.shape)
    # df = df.head()
    result = []
    all_n = df.shape[0]
    for n, line in enumerate(df.to_dict("records"), 1):
        for sentence in cut_sentence(line[key]):
            for clause in cut_clause(sentence):
                res = {
                    "id": line["id"],
                    "文件名称": line["文件名称"],
                    "审计专业类型": line["审计专业类型"],
                    "句子": clause
                }
                res.update(get_similarity(clause))
                result.append(res)
        print("正在执行第%d个文章，共%d个,剩余%d个" % (n, all_n, all_n-n))
    df_res = pd.DataFrame(result)
    df_res = df_res[df_res["similarity"] >= min_sim]
    # print(df_res.head())
    columns = ["id", "文件名称", "审计专业类型", "句子", "一级审计事项", "二级审计事项", "similarity"]
    f_dir, f_name = os.path.split(file_path)
    f_name, _ = os.path.splitext(f_name)
    f_name = f_name + "_%s.xlsx" % key
    res_dir = os.path.join(f_dir, "审计事项_简单相似度计算")
    if not os.path.isdir(res_dir):
        os.makedirs(res_dir)
    df_res[columns].to_excel(os.path.join(res_dir, f_name), header=True, index=False)


if __name__ == '__main__':
    # print(get_similarity("收入未纳入预算管理"))
    read_file(key="规则放宽的审计问题")
    read_file(key="content")
