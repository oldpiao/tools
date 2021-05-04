import re


class ReChapter5_2(object):
    """
    识别多级数字标题
    认为标题符合以下规则：
        + 认为标题不会超过两位  反例：121.  1.121 1.121.1
        + 单级标题时后面加点 正例：1. 12.
        + 多级标题最后不加点  正例：1.1 1.1.1
        + 多级标题后不可以跟数字  反例：1.12013年
    处理逻辑：
        判断文章开头是否是[0-9.．]+,且包含明显的数字单位的情况-->re_filter
        是：多级标题后不可以跟数字，仅使用re_1匹配
        否：使用多级和单级组合匹配
    规则：
        单级标题：判断不能是小数
        多级标题：判断结尾不能是数字被打断  反例：1.1.123（否则会识别到1.1.12）
    """
    def __init__(self):
        # 1. 1.  # 特例 2．2013年12月 1.26万元
        # 1.1 1.1.1  # 特例 2.2 2013年12月  1.26%你好中国  1.26万元
        self.re_filter = re.compile(r"^[0-9.．]+(%|[百万亿]|美元|元|[年月日时])", re.DOTALL)
        self.re_1 = re.compile(r'^(([0-9]{1,2})[．.])(\d+%|\d+[百万亿]*元)?', re.DOTALL)  # 匹配单级标题
        self.re_2 = re.compile(r'^(([0-9]{1,2}(?:[．.][0-9]{1,2})+))(\d+)?', re.DOTALL)  # 匹配多级标题

    def search(self, string, *args, **kwargs):
        result = self.re_filter.search(string, *args, **kwargs)
        if result is not None:
            re_list = [self.re_1]
        else:
            re_list = [self.re_2, self.re_1]
        for each_re in re_list:
            result = each_re.search(string, *args, **kwargs)
            if result is not None:
                if result.groups()[2] is not None:
                    continue
                return result
        return None


if __name__ == '__main__':
    cr_chapter_5_2 = ReChapter5_2()
    assert cr_chapter_5_2.search("1.你好中国").groups()[0] == "1."
    assert cr_chapter_5_2.search("1.1你好中国").groups()[0] == "1.1"
    assert cr_chapter_5_2.search("1.1.1你好中国").groups()[0] == "1.1.1"
    assert cr_chapter_5_2.search("1.1.1.1你好中国").groups()[0] == "1.1.1.1"
    assert cr_chapter_5_2.search("1.26万元你好中国") is None
    assert cr_chapter_5_2.search("1.26%你好中国") is None
    assert cr_chapter_5_2.search("2．2013年12月 1.26万元").groups()[0] == "2．"
    assert cr_chapter_5_2.search("2.2 2013年12月 1.26万元").groups()[0] == "2.2"
    assert cr_chapter_5_2.search("2.2013年12月 1.26万元").groups()[0] == "2."
