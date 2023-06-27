import re

from article_tree import func
from article_tree.chaper_classifier.judge_chaper import is_chapter

# re_split = re.compile(r'([^\n]*\n*)')  # 该方法可以避免空行的产生
# re_split = re.compile(r'([^\n]*)\n?')
re_split = re.compile(r'\n+')


class ChaperClassifier(object):
    """文章结构识别器"""

    def __init__(self):
        self.lines = []
        self.serials = []
        self.line_types = []
        self.status = True
        self.status_info = None

    def get_status(self):
        return {
            "status": self.status,
            "status_info": self.status_info,
        }

    @property
    def line_ts(self):
        return [serial.type_num for serial in self.serials]

    @property
    def line_nums(self):
        return [serial.zh_num for serial in self.serials]

    @property
    def line_int_nums(self):
        return [serial.int_num for serial in self.serials]

    def set_lines(self, string):
        self.lines = set_lines(string)

    def set_serials(self):
        self.serials = set_serials(self.lines)

    def set_line_types(self):
        self.line_types = set_line_types(self.line_ts)

    def init(self, string):
        """
        :param string: 文章段落
        :return:
        """
        self.set_lines(string)
        self.set_serials()
        self.set_line_types()
        return self

    def verify_and_cut_st(self):
        """验证并尝试切分未发现的段落标题，将未能正常切分开的段落标题切分出来"""
        # print(self.line_nums)
        # print([serial.st for serial in self.serials])
        for equative, serial_range, miss_nums in self.verify():
            # print(equative, serial_range, miss_nums)
            self.update_lines(serial_range, miss_nums)
        self.init('\n'.join(self.lines))
        self.verify()  # 重新验证是否缺失段落标题，更新状态
        return self

    def verify(self):
        """验证段落标题是否存在缺失"""
        result = list(verify(self.line_int_nums, self.line_types))
        if len(result) > 0:
            self.status = False
            self.status_info = "段落标题缺失"
        else:
            self.status = True
            self.status_info = None
        return result

    # def update_lines2(self, serial_range, end_num=None):
    #     """
    #     查找段落结尾是否存在未切分开的段落标题，并将其切分开
    #     :param serial_range:
    #     :param end_num: 验证当前段落标题结尾是否存在未切分的段落标题，默认为None, 表示不验证
    #     :return:
    #     """
    #     if end_num is not None:
    #         miss_st = self.serials[serial_range[0]].int2st(end_num)  # 缺失的段落标题
    #         print("尝试在段尾查找缺失的段落标题：%d: %s" % (end_num, miss_st))
    #         print(serial_range[-1], len(self.lines))
    #         for i in range(serial_range[-1], len(self.serials)):
    #             if self.serials[i].type_num == self.serials[serial_range[0]].type_num:
    #                 if 0 <= self.line_types[i] < self.line_types[serial_range[0]]:
    #                     break
    #             if self.try_update_line(i, miss_st):
    #                 break

    def update_lines(self, serial_range, miss_nums):
        """
        查找是否存在未切分开的段落标题，并将其切分开
        :param serial_range:
        :param miss_nums:
        :return:
        """
        for miss_num in miss_nums:
            re_miss_st = self.serials[serial_range[0]].int2re_st(miss_num)  # 缺失的段落标题
            print("尝试查找缺失的段落标题：%d: %s" % (miss_num, re_miss_st))
            # 如果缺失的是序号为一的段落标题，需要向前查找，直到一个段落标题为止
            if miss_num == 1:
                for i in range(0, serial_range[0])[::-1]:
                    if self.try_update_line(i, re_miss_st):  #
                        break
                    if 0 <= self.line_types[i] < self.line_types[serial_range[0]]:
                        break
            else:
                for i in range(serial_range[0], serial_range[-1] + 1):
                    if self.serials[i].type_num == self.serials[serial_range[0]].type_num:
                        if self.serials[i].int_num >= miss_num + 1:
                            break
                    if self.try_update_line(i, re_miss_st):
                        break

    def try_update_line(self, i, re_miss_st):
        """尝试查找缺失的段落标题，并更新该行"""
        miss_st = re.search(re_miss_st, self.lines[i])
        # print(self.lines[i])
        if miss_st is not None:
            print('缺失的段落标题已找到：%s：%s ' % (re_miss_st, self.lines[i][miss_st.start(1)-10: miss_st.start(1)+10]))
            self.lines[i] = self.lines[i][:miss_st.start(1)] + '\n' + self.lines[i][miss_st.start(1):]
            return True
        return False


def verify(line_int_nums, line_types):
    """验证段落是否缺失，从而发现未被切分开的段落
    + 不验证段落结尾是否存在未切分的段落
    + 不验证一级标题（0级标题），因为审计问题本身就是多个一级段落的组合，验证一级标题无意义
    因此如果要将此模块用在别的地方，要修改相关代码，使其符合自身需求
    """
    # print(line_int_nums)
    # print(line_types)
    ahead = 0
    # print(line_ts)
    for i in range(len(line_types)):
        # print(x)
        # -1为非段落标题行、0为首行，目前对于审计问题提取的段落，因此一级段落标题允许缺失
        if line_types[i] == -1:
            continue
        if line_types[i] == 0 or line_types[i] < ahead:
            ahead = line_types[i] + 1
            continue
        equative = [line_int_nums[i]]  # 同级序号
        serial_range = [i]
        ahead += 1
        for j in range(i + 1, len(line_types)):
            # 此时遇到了更高级的标题
            if 0 <= line_int_nums[j] < line_types[i]:
                break
            elif line_types[j] == line_types[i]:
                equative.append(line_int_nums[j])
                serial_range.append(j)
        miss_nums = func.find_miss_nums(equative, v_top=1)
        if len(miss_nums) != 0:
            yield equative, serial_range, miss_nums


def set_lines(string):
    return re_split.split(string)


def set_serials(lines):
    return [is_chapter.is_chapter(line) for line in lines]


def set_line_types(line_ts):
    # 每行的类型，每个数字表示该类型在chapter_types中的位置
    line_types = [-1 for _ in range(len(line_ts))]
    ahead = 0
    # print(line_ts)
    for i in range(len(line_ts)):
        # print(line_types)
        if line_types[i] != -1:
            ahead = line_types[i] + 1
            continue
        if line_ts[i] == -1:
            continue
        line_types[i] = ahead
        ahead += 1
        for j in range(i + 1, len(line_ts)):
            if 0 <= line_types[j]:
                break
            elif line_ts[j] == line_ts[i]:
                line_types[j] = line_types[i]
    return line_types
