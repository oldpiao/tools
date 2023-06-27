# 识别段落标题并对段落分句
# 该段落标题识别不可延伸到一般文档中使用，因为无法处理1.1.1这类段落标题
# 审计报告中目前来看不会出现此情况，加入后又会导致程序过于复杂，并引入小数造成的误差
from article_tree.find_chaper import FindChapter

name = "文本结构树"
version = "1.3.3"

# 例: FindChapter.open_str('一、aaa\n（一）bbb\ncccc\n（二）ddd').to_json(ensure_ascii=False, indent=1)
# 可以将传入的内容按照段落结果存储，且可以本地化为json格式，之后可以选择从json读入即可
# 例: FindChapter.open_json('一、aaa\n（一）bbb\ncccc\n（二）ddd').to_json(ensure_ascii=False, indent=1)
# open_str()
# open_dict()
# open_json()
# to_json(ensure_ascii=False, indent=1)
# to_dict()
# to_str()
# get_child()
# get_child_use_obj()
# find_sentence()

