# 词性正则规则集，匹配单个词的规则
import re

from split_words.segmente.my_tag_re.judge import *


__all__ = [
    'Rule', 'MeanAndTag', 'MeanOrTag', 'Tag', 'Tag2', 'Mean', 'Mean2',
    'Wildcard', 'Number', 'SplitRules', 'cut_rule',
]


re_mean_and_tag = re.compile(r'^(.+?)(&&)(.+?)$')  # 词性词义取并集 and ∧ \u8744
re_mean_or_tag = re.compile(r'^(.+?)(\|\|)(.+?)$')  # 词性词义取交集  or ∨  \u8743
re_mean = re.compile(r'^-[a-z0-9A-Z]$', re.U)  # 词义
re_mean2 = re.compile(r'^-(.+)-$', re.U)  # -开头，-结尾,结尾的-后面是整体的参数
re_tag_fuzzy = re.compile(r'^_[a-zA-Z@]+$', re.U)  # 词性模糊匹配
re_tag_fuzzy2 = re.compile(r'^_(.+)_$', re.U)  # 词性正则匹配
re_tag_exact = re.compile(r'^[a-zA-Z@]+$', re.U)  # 词性精确匹配
# re_wildcard = re.compile('^[.]$', re.U)
# re_number = re.compile('^\\d$', re.U)
re_m2n = re.compile(r'^(.+?){(\d+),(\d*?)}$', re.U)
re_m = re.compile(r'^(.+?){(\d+)}$', re.U)


class Rule(object):
    def __init__(self, rule, judgement):
        """
        :param rule: 拆解后的规则实体，可以是词义、词性、通配符等
        :param judgement: 规则中附带的功能实例化类，目前包含 * + {2,10} 等匹配内容个数的功能
            judge(judgement): 参数judgement为True/False，会进一步的处理成-1、0、1、2、3等
        """
        self.rule = rule
        self.judgement = judgement

    def get_status(self, word):
        return False

    def judge(self, word):
        return self.judgement.judge(self.get_status(word))


class MeanAndTag(object):
    """词性和词义同时满足条件"""
    def __init__(self, mean, tag, judgement):
        self.mean = mean
        self.tag = tag
        self.judgement = judgement

    def get_status(self, word):
        return self.tag.get_status(word) and self.mean.get_status(word)

    def judge(self, word):
        return self.judgement.judge(self.get_status(word))


class MeanOrTag(MeanAndTag):
    """词性和词义其中一个满足条件"""
    def get_status(self, word):
        return self.tag.get_status(word) or self.mean.get_status(word)


class Tag(Rule):
    """词性判断，如果词性前加_则使用模糊匹配匹配词性级别"""

    def __init__(self, rule, judgement, fuzzy=False):
        super(Tag, self).__init__(rule, judgement)
        if fuzzy:
            self.rule_len = len(self.rule)
        else:
            self.rule_len = None

    def get_status(self, word):
        return word.flag[:self.rule_len] == self.rule


class Tag2(Rule):
    """词性判断，如果词性前加_则使用模糊匹配匹配词性级别"""

    def get_status(self, word):
        return re.search(self.rule, word.flag) is not None


class Mean(Rule):
    """词义"""

    def get_status(self, word):
        return word.word == self.rule


class Mean2(Rule):
    """词义正则匹配，可以识别更多情况"""

    def get_status(self, word):
        return re.search(self.rule, word.word) is not None


class Wildcard(Rule):
    """通配符"""

    def get_status(self, word):
        return True


class Number(Rule):
    """数字,包含int型或float型的都识别"""

    def get_status(self, word):
        try:
            _ = float(word.word)  # 能够转成小数说明是数字
            return True
        except ValueError:
            return False


class SplitRules(object):
    def __init__(self, rule, freq=None, tag=None):
        self.rule = rule
        self.freq = freq
        self.tag = tag
        self.split_rule = []

        self.init()

    def append(self, rule):
        self.split_rule.append(rule)

    def init_rule(self, rule, greed=True):
        if rule[-1] == '?':
            return self.init_rule(rule[:-1], greed=False)
        if rule[-1] == '+':  # 你好+/n+/
            return rule[:-1], JudgeAdd(greed=greed)

        if rule[-1] == '*':  # 你好*/n*/
            return rule[:-1], JudgeStar(greed=greed)

        data = re_m.search(rule)
        if data is not None:  # 你好{3}/n{3}/
            rule, num = data.groups()
            num = int(num)
            return rule, JudgeNumber(num, greed=greed)

        data = re_m2n.search(rule)
        if data is not None:  # 你好{1,3}/n{1,3}/
            rule, begin, end = data.groups()
            begin = int(begin)
            if end != '':
                end = int(end)
            else:
                end = None
            return rule, JudgeRange(begin, end, greed=greed)

        return rule, JudgeBase(greed=greed)  # 你好/n/

    def cut_rule(self):
        """将词性正则规则拆分成一个个成分，可以处理内容中带“/”的情况"""
        # cut_rules = list(cut_rule(self.rule))
        # print(cut_rules)
        return cut_rule(self.rule)

    def init(self):
        """规则使用/分隔,且暂不解决规则中含有/的问题
        纯字母认为是精确匹配词性
        首字母为'_'且之后字母符合词性的认为是通配方式匹配词性如：_n 通配['n', 'nr', 'nrj', ...],
        首字母是'-'且之后是字母的认为是匹配词义
        三种都匹配不到的认为是匹配词义
        """
        # 此处可以加转义字符处理，至少可以加转义'/'(\/)处理
        # 目前规则中不允许出现字符/，因为未对其做转义处理
        for each_rule in self.cut_rule():
            each_rule2, judgement = self.init_rule(each_rule)  # 扩展功能匹配,例: n+/你好*/
            self.append(self.get_rule_model(each_rule2, judgement))

    def get_rule_model(self, each_rule2, judgement):
        """
        获取单个字符的匹配规则模型
        :param each_rule2: 单个字符的匹配规则
        :param judgement:  单个字符的匹配附加规则 * + ? {2} {2,} {2,5}等
        :return:
        """
        result = re_mean_and_tag.search(each_rule2)
        if result is not None:
            return MeanAndTag(
                self.get_rule_model(result.groups()[0], judgement),
                self.get_rule_model(result.groups()[2], judgement),
                judgement,
            )
        result = re_mean_or_tag.search(each_rule2)
        if result is not None:
            return MeanOrTag(
                self.get_rule_model(result.groups()[0], judgement),
                self.get_rule_model(result.groups()[2], judgement),
                judgement,
            )
        if re_mean.search(each_rule2) is not None:  # 词义正则匹配,例: -你好/-n/-abc
            return Mean(each_rule2[1:], judgement)
        elif re_mean2.search(each_rule2) is not None:  # 词义正则匹配,例: -^不.+-   -^不.+-{2,}
            return Mean2(each_rule2[1:-1], judgement)
        elif re_tag_fuzzy2.search(each_rule2) is not None:  # 词性正则模糊匹配,例: _^v?n_/  # 匹配名词或动名词
            return Tag2(each_rule2[1:-1], judgement)
        elif re_tag_fuzzy.search(each_rule2) is not None:  # 词性模糊匹配,例: _n/  # 匹配词性首字母为n的词即所有名词
            return Tag(each_rule2[1:], judgement, fuzzy=True)
        elif re_tag_exact.search(each_rule2) is not None:  # 词性精确匹配,例: n/
            return Tag(each_rule2, judgement)
        # elif re_wildcard.search(each_rule2):
        elif each_rule2 == '.':  # 通配符匹配,例: ./
            return Wildcard(each_rule2, judgement)
        # elif re_number.search(each_rule2):
        elif each_rule2 == '\\d':  # 数字匹配, 例: 123/
            return Number(each_rule2, judgement)
        else:  # 词义匹配,例: 你好/
            return Mean(each_rule2, judgement)

    def init_judgement(self):
        # 将所有切块后的规则的状态都初始化，以免影响下一次使用
        for each_rule in self.split_rule:
            each_rule.judgement.init()

    def get_result(self, words, wn):
        """词性正则最终获取到结果的长度，然后用该方法从words中提取出这部分词"""
        # 新增该行，以修复模型匹配后未初始化，导致之后匹配异常的情况
        # 例：n{2,}第一次匹配必须两个名词，之后一个名词的也会被匹配到
        self.init_judgement()
        new_word = ''
        if wn is None:
            return None, 0
        if wn == 0:
            # 类似a*?这样的规则，一个字符都未匹配到，但又不属于报错，
            # 设置成带词性的空字符又不合适，因此目前也按未匹配到处理
            return None, 0
        for word in words[:wn]:
            new_word += word.word
        # self.tag or default_tag, words[wn-1].flag
        return (new_word, self.tag, words[wn-1].flag), wn

    def match(self, words):
        """
        研究可以解决非贪婪匹配和动态规划问题的算法，
        弄出来之前使用judge方法: ?功能暂时无法使用，n*/n+形式的规则依然会报错
        :param words:
        :return:
        """
        len_words = len(words)
        len_rules = len(self.split_rule)
        new_word, rn, wn, judgement = {}, 0, 0, -1
        new_word[rn] = 0
        while rn < len_rules:
            # print(rn, wn, self.rule, self.tag, words[:wn])
            if wn >= len_words:  # 当words处理完时
                # 规则不一定已经处理完了
                over = True
                for each_rn in range(rn, len_rules):
                    # 判断剩余规则
                    # 只要有一个规则未能匹配到足够的词，就返回空
                    if not self.split_rule[each_rn].judgement.is_ok():
                        rn_wn = self.borrow(rn+1, wn)
                        # 新增判断wn,rn长度，由于此处有可能会存在字符超限的情况一般存在于wn中
                        if rn_wn is None or wn >= len_words or rn >= len_rules:
                            return self.get_result(words, None)
                        else:
                            (rn, wn) = rn_wn
                            over = False
                            break
                # 否则认为规则依然匹配到了结果
                if over:
                    return self.get_result(words, wn)
            judgement = self.split_rule[rn].judge(words[wn])
            if judgement == -2:
                rn += 1
            elif judgement == -1:
                wn -= self.split_rule[rn].judgement.init_success()
                rn_wn = self.borrow(rn, wn)
                if rn_wn is None:
                    return self.get_result(words, None)
                else:
                    (rn, wn) = rn_wn
            elif judgement == 0:
                rn += 1
            elif judgement == 1:
                rn += 1
                wn += 1
            elif judgement == 2:
                wn += 1
            elif judgement == 3:
                rn += 1
                wn += 1
        return self.get_result(words, wn)

    def borrow(self, rn, wn):
        """向前一个规则借位"""
        while True:
            if rn - 1 < 0:
                return None
            move_wn = self.split_rule[rn - 1].judgement.borrow()
            if move_wn == -2:
                wn -= 1
                break
            elif move_wn == -1:
                rn -= 1
                break
            else:
                rn -= 1
                wn -= move_wn
        return rn, wn


def cut_rule(rule):
    # 是否处于转义状态，处理转义符后要将转义符去除，因为这里是自定义的转义场景
    # 仅对“\”、“/”两个符号转义
    status = False
    begin = 0
    for n, i in enumerate(rule):
        if i == r'/':
            if not status:
                yield rule[begin:n]
                begin = n + 1
                status = False
                continue
        elif i == '\\':
            status = not status
        elif status:
            status = not status
    if len(rule) - begin > 0:
        yield rule[begin: len(rule)]


# def cut_rule(rule):
#     rules = rule.split(r'/')
#     new_rules = []
#     n = 0
#     print(rules)
#     while n < len(rule):
#         print(rules[n])
#         if rules[n][-1] == '\\' and n + 1 < len(rule):
#             rules[n + 1] = rules[n][:-1] + rule[n + 1]
#         else:
#             new_rules.append(rule[n])
#         n += 1
#     return new_rules


def ceshi_cut_rule():
    # print(list(cut_rule(r'aa/bb/cc')))
    # print(list(cut_rule(r'aa/bb\/cc')))
    # print(list(cut_rule(r'aa/bb\\/cc')))
    print(list(cut_rule(r'aa/dd\\/cc')))
    print(list(cut_rule(r'aa/\dd\\/cc')))
    a = list(cut_rule(r'aa/\dd\\/cc'))
    print(a)
    print(re.search(a[1], 'aa/1d\\'))
    print(re.compile(a[1]))
    print(re.compile(r'\dd\\'))


if __name__ == '__main__':
    ceshi_cut_rule()
