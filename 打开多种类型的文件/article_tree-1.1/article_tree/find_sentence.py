import json
import re

re_sentence = re.compile(r'([^。？?！!\r\n\t]+[。？?！!\r\n\t]*)')  # 句子结束符


class FindSentence(object):

    def __init__(self, sentences):
        self.sentences = sentences

    @classmethod
    def open_str(cls, string: str):
        return cls(re_sentence.findall(string))

    @classmethod
    def open_dict(cls, data_dict: dict):
        return cls(data_dict)

    @classmethod
    def open_json(cls, data_json: str):
        """ 从该模块处理后生成的json数据中读入信息
        :param data_json 该模块处理后生成的json数据
        :return: 模型初始化
        """
        data_dict = json.loads(data_json)
        return cls.open_dict(data_dict)

    def to_str(self):
        """输出文本数据"""
        return ''.join(self.sentences)

    def to_dict(self):
        """输出当前数据结构"""
        # return {"sentences": self.sentences}
        return self.sentences

    def to_json(self, ensure_ascii=True, indent=None, *args, **kwargs):
        return json.dumps(self.to_dict(), ensure_ascii=ensure_ascii, indent=indent, *args, **kwargs)

    def find_sentence(self, f_obj):
        """ 通过关键词查找该词在文章中的哪一句中
        :param f_obj: 查找方法，该方法的输入为文章中的一句话，可以用lamada实现
        :return: dict结构的返回结果，当前层num为该内容所在的句，line为该句话
        """
        for n, sentence in enumerate(self.sentences, 0):
            if f_obj(sentence):
                return {
                    "num": n,  # 方便反向查找该句话的出处
                    "sentence": sentence
                }

