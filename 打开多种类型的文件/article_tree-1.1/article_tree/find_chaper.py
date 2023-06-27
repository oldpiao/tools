import json

from article_tree.chaper_classifier import chaper_classifier
from article_tree.find_sentence import FindSentence


class FindChapter(object):
    """设置文章中的一级标题"""

    def __init__(self, lines, line_types, line_nums, status):
        """
        初始化可以采用文本初始化，或json初始化，json为该方法生成的本地化保存的结果
        :param lines: list, [FindSentence, ...]
        :param line_types: list, [标题格式在chapter_types中的存储位置, ...]
        :param line_nums: list, 每行的段落标题序号，没有的为None
        :param status: dict, {"status": True/Faslse, "status_info": "错误信息"}
        """
        self.lines = lines
        self.line_types = line_types
        self.line_nums = line_nums
        self.status = status

    @classmethod
    def open_str(cls, string: str):
        """ 识别段落标题
        :param string: 文本数据，回车换行
        :return: 模型初始化
        """
        # 当前的正则匹配的最后一个一定是一个空字符，因此将其删除
        # lines = re_split.findall(string)[:-1]  # 分成段
        cc = chaper_classifier(string)
        # 验证分段正确性，并处理
        # print(cc.line_nums)
        # print(cc.line_ts)
        # print(cc.line_types)
        # print(cc.status, cc.status_info)
        # line_types, chapter_types, status, status_info
        # 拆分内容与标题在一起的段，并初始化段落为行对象
        new_lines, new_line_types, new_line_nums = [], [], []
        for line, line_type, line_num in zip(cc.lines, cc.line_types, cc.line_nums):
            fs = FindSentence.open_str(line)
            if line_type != -1 and len(fs.sentences) > 1:
                new_lines.append(FindSentence(fs.sentences[:1]))
                new_line_types.append(line_type)
                new_line_nums.append(line_num)
                new_lines.append(FindSentence(fs.sentences[1:]))
                new_line_types.append(-1)
                new_line_nums.append(None)
            else:
                new_lines.append(fs)
                new_line_types.append(line_type)
                new_line_nums.append(line_num)
        # print(new_line_nums)
        # print(new_line_types)
        # for a, b, c in zip(new_line_types, new_line_nums, new_lines):
        #     print("%s\t%s\t\t%s" % (a, b, c.to_str()))
        return cls(new_lines, new_line_types, new_line_nums, cc.get_status())

    @classmethod
    def open_dict(cls, data_dict: dict):
        lines = [FindSentence.open_dict(line) for line in data_dict['data']['lines']]
        return cls(
            lines=lines, line_types=data_dict['data']['line_types'],
            line_nums=data_dict['data']['line_nums'],
            status=data_dict['status'],
        )

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
        # 需要结合包含回车的分段方法使用，还原回去的文本依然是原来的结构
        # return ''.join([line.to_str() for line in self.lines])
        # 需要结合不包含回车的分段方法使用，还原回去的文本带子标题的会被切开
        return '\n'.join([line.to_str() for line in self.lines])

    def to_dict(self):
        """输出当前数据结构"""
        return {
            "status": self.status,
            "data": {
                "lines": [line.to_dict() for line in self.lines],
                "line_types": self.line_types,
                "line_nums": self.line_nums,
            }}

    def to_json(self, ensure_ascii=True, indent=None, *args, **kwargs):
        return json.dumps(self.to_dict(), ensure_ascii=ensure_ascii, indent=indent, *args, **kwargs)

    def get_child_end_n(self, n, single_p=True):
        """ 获取当前段落的子段落结束位置，切片时需要+1"""
        now_type = self.line_types[n]
        if n == len(self.line_types) - 1:  # 最后一行
            return n
        elif now_type == -1:
            if single_p:
                return n
            for i, line_type in enumerate(self.line_types[n + 1:], n + 1):
                if line_type != -1:
                    return n
        else:
            for i, line_type in enumerate(self.line_types[n+1:], n+1):
                if line_type != -1 and line_type <= now_type:
                    return i - 1
        return len(self.line_types) - 1

    def get_child(self, n, single_p=True):
        """ 获取当前段落的子段落
        :param n: 当前段落的行号
        :param single_p: 非段落标题段落（-1）是否作为单独的段不获取之后的段落作为其段落，默认不获取
        :return: 字段落的FindChapter实例化对象
        """
        end_n = self.get_child_end_n(n, single_p=single_p)
        return FindChapter(
            lines=self.lines[n: end_n+1], line_types=self.line_types[n: end_n+1],
            line_nums=self.line_nums[n: end_n+1],
            status=self.status,
        )

    def get_child_use_obj(self, f_obj, single_p=True):
        """
        使用行文本获取其子段落, 先定位到该行，再获取其子段落
        例：
            fc = FindChapter.open_str(一、XXX\n（一）YYY\nZZZ)
            fc.get_child_use_obj(f_obj=lambda x: 'XXX' in x.to_str())
        :param f_obj: 查找方法，该方法的输入为文中的一段内容，可以用lamada实现
        :param single_p: 非段落标题段落（-1）是否作为单独的段不获取之后的段落作为其段落，默认不获取
        :return:
        """
        for n, each_line in enumerate(self.lines):
            if f_obj(each_line):
                return self.get_child(n, single_p=single_p)
        return None

    def find_sentence(self, f_obj):
        """ 通过关键词查找该词在文章中的哪一句中，限定条件，信息仅存在于一句话中
        :param f_obj: 查找方法，该方法的输入为文章中的一句话，可以用lamada实现
        :return: 嵌套dict结构的返回结果，当前层num为该内容所在的段，line为该句话的信息，也是dict结构
        """
        for n, line in enumerate(self.lines):
            sentence = line.find_sentence(f_obj)
            if sentence is not None:
                return {
                    "num": n,  # 方便用来查找该内容所在的段落
                    "line": sentence
                }
        return None
