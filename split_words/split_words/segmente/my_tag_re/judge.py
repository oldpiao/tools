# 词性正则符号功能实现
__all__ = [
    'JudgeBase', 'JudgeStar', 'JudgeAdd', 'JudgeNumber', 'JudgeRange'
]


class JudgeBase(object):

    def __init__(self, minimum=1, maximun=1, is_true=1, is_false=-1, greed=True):
        self.default_minimum = minimum
        self.default_maximun = maximun
        self.default_is_true = is_true
        self.default_is_false = is_false
        self.default_now_status = None
        self.default_success = 0
        self.default_greed = greed
        if greed:
            self.default_judge = self.judge_greed
        else:
            self.default_judge = self.judge_not_greed
        self.init()

    def init(self):
        self.minimum = self.default_minimum
        self.maximun = self.default_maximun
        self.is_true = self.default_is_true
        self.is_false = self.default_is_false
        self.now_status = None
        self.success = 0
        self.greed = self.default_greed
        self.judge = self.default_judge

    def borrow(self):
        """借位，后面规则匹配不上，向前面的规则求助
        :return:
                -2:  贪婪匹配，有多余位可借
                n:  贪婪匹配无多于位可借或非贪婪匹配已经到最大位数
                -1: 非贪婪匹配，未到最大位数
        """
        if self.greed is False and self.now_status in [-2, 3]:
            # 非贪婪算法
            # 可以向后匹配, 使用该规则向后多匹配一位，字符串不移动
            return -1
        elif self.greed is True and self.success > self.minimum:
            # 贪婪算法
            # 可以借位，借一位给后面规则，当前规则匹配到的内容减少一位，字符串向前移动一位
            self.success -= 1
            return -2
        else:
            # 贪婪算法规则无法借位或非贪婪算法无法向后匹配
            # 规则匹配到的内容置空，字符串向前移动该规则匹配到的位数
            return self.init_success()

    def is_ok(self):
        """验证当前规则是否成功匹配到了足够数量的字符，
        用于在字符串处理完，但规则还未用完时验证剩余规则是否已经完整
        """
        if self.maximun is None:
            return self.success >= self.minimum
        else:
            return self.maximun >= self.success >= self.minimum

    def init_success(self):
        n = self.success
        self.success = 0
        return n

    def judge_not_greed(self, judgment):
        self.is_false = 0
        return self.judge_greed(judgment)

    def judge_greed(self, judgment):
        """
        :param judgment: 判断结果,True or False
        :return:
            -2  # 未判断是否匹配成功，且按匹配失败处理，但在之后如有需要可以继续使用该规则往后匹配（非贪婪）
            -1  # 匹配失败
            0  # 匹配失败，继续使用该词和后续规则匹配
            1  # 匹配成功
            2  # 匹配成功，且继续使用该字段匹配（贪婪）
            3  # 匹配成功，但不再使用该字段继续匹配，且之后如有需要可以继续用该规则继续往后匹配（非贪婪）
        """
        if judgment:
            self.success += 1
            self.now_status = self.is_true
        else:
            self.now_status = self.is_false
        return self.now_status


class JudgeAdd(JudgeBase):

    def __init__(self, minimum=1, maximun=None, is_true=2, is_false=0, greed=True):
        super(JudgeAdd, self).__init__(minimum=minimum, maximun=maximun, is_true=is_true, is_false=is_false, greed=greed)

    def judge_not_greed(self, judgment):
        self.is_true = 3
        return self.judge_greed(judgment)

    def judge_greed(self, judgment):
        """至少要有一次匹配成功，因此当首次匹配即为失败时返回-1，其他时候失败返回0"""
        if judgment:
            self.success += 1
            self.now_status = self.is_true
        else:
            if self.success <= 0:  # 一次都没成功过，则算匹配失败
                self.now_status = -1
            else:  # 至少匹配成功了一次，并不算失败，只是结束
                self.now_status = self.is_false
        return self.now_status


class JudgeStar(JudgeBase):

    def __init__(self, minimum=0, maximun=None, is_true=2, is_false=0, greed=True):
        super(JudgeStar, self).__init__(minimum=minimum, maximun=maximun, is_true=is_true, is_false=is_false, greed=greed)
        self.first = True

    def judge_not_greed(self, judgment):
        self.is_true = 3
        if self.first:
            self.first = False
            self.now_status = -2
            return self.now_status
        return self.judge_greed(judgment)

    def judge_greed(self, judgment):
        if judgment:
            self.success += 1
            self.now_status = self.is_true
        else:
            self.now_status = self.is_false
        return self.now_status


class JudgeNumber(JudgeBase):

    def __init__(self, num, is_true=2, is_false=-1, greed=True):
        super(JudgeNumber, self).__init__(minimum=num, maximun=num, is_true=is_true, is_false=is_false, greed=greed)
        self.num = num

    def judge_not_greed(self, judgment):
        # 该方法无贪婪非贪婪之分，为保证与其他算法结构相同，保留了该参数
        # 该参数使用非贪婪匹配时并无相应效果
        return self.judge_greed(judgment)

    def judge_greed(self, judgment):
        """该方法为精确匹配，无贪婪非贪婪之分,因此直接覆盖贪婪算法判断"""
        if self.success == self.num:
            self.now_status = 0
        elif judgment:
            self.success += 1
            self.now_status = self.is_true
        else:
            self.now_status = self.is_false
        return self.now_status


class JudgeRange(JudgeBase):

    def __init__(self, begin, end=None, is_true=2, is_false=0, greed=True):
        super(JudgeRange, self).__init__(minimum=begin, maximun=end, is_true=is_true, is_false=is_false, greed=greed)
        self.begin = begin
        self.end = end
        self.is_false2 = -1
        self.is_true2 = 2

    def judge_not_greed(self, judgment):
        self.is_true = 3
        return self.judge_greed(judgment)

    def judge_greed(self, judgment):
        # 从">"改为">=",否则{3,}匹配的最少要有4个词
        if self.success >= self.begin:
            self.is_false2 = self.is_false
            self.is_true2 = self.is_true
        else:  # 防止在借位的时候，该数无法变成-1
            self.is_false2 = -1
            self.is_true2 = 2
        if self.end is not None and self.success >= self.end:
            self.now_status = 0
        elif judgment:
            self.success += 1
            self.now_status = self.is_true2
        else:
            self.now_status = self.is_false2
        return self.now_status

