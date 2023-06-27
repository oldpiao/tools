from article_tree import FindChapter


tree = FindChapter.open_str('一、aaa\n（一）bbb\ncccc\nddddd\n（二）ddd')
# 可以将传入的内容按照段落结果存储，且可以本地化为json格式，之后可以选择从json读入即可
# tree = FindChapter.open_json('一、aaa\n（一）bbb\ncccc\n（二）ddd').to_json(ensure_ascii=False, indent=1)
# tree.open_str()
# tree.open_dict()
# tree.open_json()
print(tree.to_json(ensure_ascii=False, indent=1))
# tree.to_dict()
# tree.to_str()
print(tree.get_child(1).to_dict())
# tree.get_child_use_obj()
# tree.find_sentence()
