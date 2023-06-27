import re

from article_tree import func


class ReChapter5_2(object):

    def __init__(self):
        # 1. 1.  # 特例 2．2013年12月 1.26万元
        self.re_1 = re.compile(r'^(([0-9]{1,2})[．.])(\d+%|\d+[百万亿]*元)?', re.DOTALL)

    def search(self, string, *args, **kwargs):
        result = self.re_1.search(string, *args, **kwargs)
        if result is not None:
            if result.groups()[2] is not None:
                return None
            return result
        return result


class ReChapter5_3(object):
    """1. 1.1 1.1.1"""
    def __init__(self):
        # 1. 1.  # 特例 2．2013年12月 1.26万元
        self.re_1 = re.compile(r'^(((?:(?:\d{1,2})[．.])*(?:\d{1,2}))[．.]?)(\d+%|\d+[百万亿]*元|\d+[年月日]|\d+)?', re.DOTALL)
        self.re_2 = re.compile(r'^(((?:(?:\d{1,2})[．.])*(?:\d))[．.])(\d+%|\d+[百万亿]*元|\d+[年月日]|\d+)?', re.DOTALL)

    def search(self, string, *args, **kwargs):
        result = self.re_1.search(string, *args, **kwargs)
        if result is not None:
            if result.groups()[2] is not None:
                if result.groups()[1][-1] in "．.":
                    return result
                else:
                    return self.re_2.search(string, *args, **kwargs)
            return result
        return result


re_chapter0 = re.compile(r'^(([零一二三四五六七八九十]+)、)', re.DOTALL)  # 一、
re_chapter1 = re.compile(r'^([（(]([零一二三四五六七八九十]+)[)）])', re.DOTALL)  # （一）(一)
# re_chapter2 = re.compile(r'^([零一二三四五六七八九十]+)', re.DOTALL)  # 一 二
re_chapter2 = re.compile(r'^(([零一二三四五六七八九十]+)是)', re.DOTALL)  # 一是 二是
re_chapter3 = re.compile(r'^([（(]([0-9]+)[）)])', re.DOTALL)  # （1） (1)
re_chapter4 = re.compile(r'^(([0-9]{1,2})[）)])', re.DOTALL)  # 1） 1)
re_chapter5_1 = re.compile(r'^(([0-9]{1,2})[、])', re.DOTALL)  # 1、
re_chapter5_2 = ReChapter5_2()  # 1. # 特例 1. 1.23亿元
re_chapter5_3 = ReChapter5_3()  # 1. 1.1 1.1.1  # 特例
re_chapter6_1 = re.compile(r'^(([㊀-㊉]))', re.DOTALL)  # ['㊀', '㊁', '㊂', '㊃', '㊄', '㊅', '㊆', '㊇', '㊈', '㊉']
re_chapter6_2 = re.compile(r'^(([㈠-㈩]))', re.DOTALL)  # ['㈠', '㈡', '㈢', '㈣', '㈤', '㈥', '㈦', '㈧', '㈨', '㈩']
# ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩', '⑪', '⑫', '⑬', '⑭', '⑮', '⑯', '⑰', '⑱', '⑲', '⑳']
re_chapter6_3 = re.compile(r'^(([①-⑳]))', re.DOTALL)
re_chapter6_4 = re.compile(r'^(([a-z])[.])', re.DOTALL)  # a. b.
re_chapter6_5 = re.compile(r'^([（(]([a-z])[）)])', re.DOTALL)  # （a） (b)


__all__ = ['ISChapter', 'is_chapter']


class SerialNone(object):
    """无序号，为了和有序号的接口相同"""
    def __init__(self, zh_num=None, st=None, type_num=-1.0, int_num=-1, num_lis=None):
        """
        :param zh_num: 中文序号
        :param st: 段落序号带附加的点或括号等
        :param type_num: 类型序号，属于哪一类序号
        """
        self.zh_num = zh_num
        self.st = st
        self.type_num = type_num
        self.int_num = int_num
        self.num_lis = num_lis or list()

    def __str__(self):
        return "数字序号：【{}】中文序号：【{}】完整序号：【{}】序号级别：【{}】".format(
            res.int_num, res.zh_num, res.st, res.type_num)

    def del_num(self, sentence):
        """传入原句去除原句中的序号"""
        return sentence


class SerialBase(SerialNone):
    """序号,基础类"""

    def int2zhnum(self, int_num):
        return str(int_num)

    def int2st(self, int_num):
        return self.st.replace(self.zh_num, self.int2zhnum(int_num))

    def int2re_st(self, int_num):
        """
        :param int_num:
        :return: 正则匹配时的规则，str
        """
        st = self.int2st(int_num)
        st = re.sub(r'([.()[?*$^\\}])', r'\\\1', st)
        return "(%s)" % st

    def del_num(self, sentence):
        """传入原句去除原句中的序号"""
        return sentence[len(self.st):]


class SerialInt(SerialBase):
    pass


class SerialInt2(SerialInt):
    pass
    # def int2re_st(self, int_num):
    #     return r'[^0-9]%s' % super(SerialInt2, self).int2re_st(int_num)


class SerialInt3(SerialInt):

    def int2re_st(self, int_num):
        # raise Exception("当前模块暂不支持该方法，请详细调试后使用！")
        st = "[．.]".join([str(i) for i in self.num_lis[:-1] + [int_num]])
        return "(%s)" % st
        # return r'[^0-9]%s' % super(SerialInt3, self).int2re_st(int_num)


class SerialZH(SerialBase):

    def int2zhnum(self, int_num):
        return func.int2chnum(int_num)


class SerialUn1(SerialBase):

    def int2zhnum(self, int_num):
        return chr(ord('㈠')+int_num-1)


class SerialUn2(SerialBase):

    def int2zhnum(self, int_num):
        return chr(ord('㊀')+int_num-1)


class SerialUn3(SerialBase):

    def int2zhnum(self, int_num):
        return chr(ord('①')+int_num-1)


class SerialUn4(SerialBase):

    def int2zhnum(self, int_num):
        return chr(ord('a')+int_num-1)


class SerialInit(object):
    """将初始化方法集中在一起"""
    @classmethod
    def init_none(cls):
        """无序号"""
        return SerialNone(None, None, -1, -1)

    @classmethod
    def init_int(cls, zh_num=None, st=None, type_num=-1):
        """数字型序号: （1）"""
        return SerialInt(zh_num, st, type_num, int(zh_num))

    @classmethod
    def init_int2(cls, zh_num=None, st=None, type_num=-1):
        """数字型序号: 1、|1.|1）"""
        return SerialInt2(zh_num, st, type_num, int(zh_num))

    @classmethod
    def init_int3(cls, zh_num=None, st=None, type_num=-1):
        """数字型序号: 1.|1.1|1.1.1）"""
        nums = re.findall(r"\d+", zh_num)
        assert len(nums) >= 1
        # print(zh_num, nums)
        type_num = type_num+(len(nums)-1)*0.1
        return SerialInt3(zh_num, st, type_num, int(nums[-1]), num_lis=list([int(i) for i in nums]))

    @classmethod
    def init_zh(cls, zh_num=None, st=None, type_num=-1):
        """中文序号: 一、 | （一）"""
        int_num = func.chnum2int(zh_num)
        if int_num is None:
            return cls.init_none()
        return SerialZH(zh_num, st, type_num, int_num)

    @classmethod
    def init_un1(cls, zh_num=None, st=None, type_num=-1):
        """特殊的unicode编码序号: ㈠"""
        return SerialUn1(zh_num, st, type_num, ord(zh_num) - ord('㈠') + 1)

    @classmethod
    def init_un2(cls, zh_num=None, st=None, type_num=-1):
        """特殊的unicode编码序号: ㊀"""
        return SerialUn2(zh_num, st, type_num, ord(zh_num) - ord('㊀') + 1)

    @classmethod
    def init_un3(cls, zh_num=None, st=None, type_num=-1):
        """特殊的unicode编码序号: ①"""
        return SerialUn4(zh_num, st, type_num, ord(zh_num) - ord('①') + 1)

    @classmethod
    def init_un4(cls, zh_num=None, st=None, type_num=-1):
        """特殊的unicode编码序号: a"""
        return SerialUn4(zh_num, st, type_num, ord(zh_num) - ord('a') + 1)


class ISChapter(object):

    def __init__(self):
        # 规则与该规则输出结果的格式
        self.re_chapters = [
            [re_chapter0, SerialInit.init_zh],
            [re_chapter1, SerialInit.init_zh],
            [re_chapter2, SerialInit.init_zh],
            [re_chapter3, SerialInit.init_int],
            [re_chapter4, SerialInit.init_int2],
            [re_chapter5_1, SerialInit.init_int2],
            # [re_chapter5_2, SerialInit.init_int2],
            [re_chapter5_3, SerialInit.init_int3],
            [re_chapter6_1, SerialInit.init_un1],
            [re_chapter6_2, SerialInit.init_un2],
            [re_chapter6_3, SerialInit.init_un3],
            [re_chapter6_4, SerialInit.init_un4],
            [re_chapter6_5, SerialInit.init_un4],
        ]

    def is_chapter(self, line):
        """ 判断当前行是否为段落标题
        :param line: 一行文本
        :return: [段落标题类型，标题序号], -1代表非段落标题
        """
        # line = re.sub(r'\s', r'', line)
        for n, (re_chapter, serial) in enumerate(self.re_chapters, 0):
            chapter_num = re_chapter.search(line)
            if chapter_num is not None:
                # print(chapter_num.groups())
                return serial(zh_num=chapter_num.groups()[1], st=chapter_num.groups()[0], type_num=n)
        return SerialInit.init_none()


is_chapter = ISChapter()


if __name__ == '__main__':
    for text in [
        # "12．2013年12月 1.26万元",
        "1.今天天气正好",
        "（1）今天天气正好",
        "(1)今天天气正好",
        "一、今天天气正好",
        "1.1 2013年12月 1.26万元",
        "1.1.12.1.2 2013年12月 1.26万元",
        "1.1.12.1. 2013年12月 1.26万元",
    ]:
        res = is_chapter.is_chapter(text)
        print(res)
        print(res.int2re_st(2))
        # print(text)
        # print(res)
