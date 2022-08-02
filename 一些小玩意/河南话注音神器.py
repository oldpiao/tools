# -*- coding:utf-8 -*-
# pip install pypinyin
from pypinyin import pinyin

norm_ch = "āáǎàōóǒòēéěèīíǐìūúǔùǖǘǚǜü"
# 2413
henan_ch = "áàāǎóòōǒéèēěíìīǐúùūǔǘǜǖǚ"
# print(dict(zip(norm_ch, henan_ch)))
norm2henan_map = {'ā': 'á', 'á': 'à', 'ǎ': 'ā', 'à': 'ǎ',
                  'ō': 'ó', 'ó': 'ò', 'ǒ': 'ō', 'ò': 'ǒ',
                  'ē': 'é', 'é': 'è', 'ě': 'ē', 'è': 'ě',
                  'ī': 'í', 'í': 'ì', 'ǐ': 'ī', 'ì': 'ǐ',
                  'ū': 'ú', 'ú': 'ù', 'ǔ': 'ū', 'ù': 'ǔ',
                  'ǖ': 'ǘ', 'ǘ': 'ǜ', 'ǚ': 'ǖ', 'ǜ': 'ǚ'}


def run(string):
    res = []
    for word, zh_pinyin in zip(string, pinyin(string)):
        henan_pinyin = "".join([norm2henan_map.get(i, i) for i in zh_pinyin[0]])
        # print(word, henan_pinyin)
        res.append({"word": word, "zh": zh_pinyin, "henan": henan_pinyin})
    print(" ".join([i["henan"] for i in res]))
    print("\t".join([i["word"] for i in res]))
    return res


if __name__ == '__main__':
    run("小葵花河南话课堂开课啦，孩子河南话老说不好，多半是拼音标错了！")
    run("中华人民共和国")
    run("咏鹅：鹅，鹅，鹅，曲项向天歌。白毛浮绿水，红掌拨清波。")
    run("而税款竟然是零！！")


