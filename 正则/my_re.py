# -*- coding: utf-8 -*-
# 各个模块间通用的正则
import re

name = "通用正则"
version = '2.0.0'

re_ch_str = r'[\u4E00-\u9FA5]'
re_chinese = re.compile(re_ch_str)
re_english = re.compile(r'^[a-zA-Z0-9_]+$')

re_file = re.compile(r'\.(docx?|pdf|zip|rar|wps)', re.IGNORECASE)
re_file2 = re.compile(r'\.(docx?|pdf|wps)', re.IGNORECASE)
re_file3 = re.compile(r'\.(zip|rar)', re.IGNORECASE)

re_null_char = re.compile(r'\s')  # 空字符计算文本长度时使用该方法先去除空字符

# 有的“附件”会写成“除件”，仅做记录未处理
# re_affix1 = re.compile(r'^(\d+[^\u4E00-\u9FA5]*)?(附件|附表|附录|相关链接)')
re_affix1 = re.compile(r'^(\d+[^\u4E00-\u9FA5]*)?(附[件录表])')
re_affix2 = re.compile(r'^(\d+[^\u4E00-\u9FA5]*)?(附表)')

re_tu_table = re.compile('[图表]')  # 识别附件是否是图或表
re_catalog1 = re.compile(r'[\-.。•]{7,}|[…]{3,}')  # 识别目录，文章分类用（目前没用上）
re_catalog2 = re.compile(r'[\-]{3,}|[.。•]{2,}|[…]')  # 识别目录，标题识别用，可能会误识别，但依然是不是标题或一级标题
re_catalog3 = re.compile(r'^\s*目\s*录\s*$|^contents?$', re.IGNORECASE)

res_sjs_keyword = [
    re.compile(r'审计署\d{4}年第\d+号'),  # 审计署关键词1
    re.compile(r'审计署第\d+号公告')  # 审计署关键词2
]

re_pdf_read_error = re.compile(r'\(cid:\d+\)')  # PDF解析失败的文件

re_punctuation = re.compile(r'[,，。!！?？;；]')  # 标题中不会出现的标点符号，去除“.”因为存在是小数点的可能
re_punctuation2 = re.compile(r'[,，。!！?？;；:：]')  # 标题中不会出现的标点符号，去除“.”因为存在是小数点的可能
re_punctuation_over = re.compile(r'[.。!！?？]\s*$')  # 结束符结尾，一定不是标题

# 发布日期
re_is_release_time = re.compile(r'^[0-9\-a-zA-Z○〇ОＯ零一二三四五六七八九十\\/()（）\[\]【】年月日公告]+$')
# 段落标题
# １．亚洲开发银行贷款甘肃省天水市城市基础设施建设项目（请点击下载查看）
# [\uff10-\uff19] == [０-９]  # 特殊格式的数字
# 2016、2017年
re_sts = re.compile(r'(^[0-9\uff10-\uff19]{1,2}[.．、]|'
                    r'^[零一二三四五六七八九十]+、|'
                    r'^[(（][零一二三四五六七八九十]+[）)]|'
                    r'^[(（]\d+[）)]|'
                    r'^[\u3220-\u3229\u3280-\u3289]|'
                    r'^[IiVvxⅴ]+\.)(.*?)$')  # i. ii. iii. III. IV.
# 冒号
re_colon = re.compile(r'[:：]')
# 在标题中发现文件号
# 发现文件号
re_file_number1 = re.compile(r'\d{4}年第\d+号审?计?结?果?公?告?([(（]总第\d+号[）)])?([(（][上中下][）)])?')
# 在标题中发现文件号
# 2018年第3号审计结果公告：2017年度全省地方税收征收管理情况审计结果
re_file_number2 = re.compile(r'\d{4}年?第\d+号审?计?结?果?公?告?([(（]总第\d+号[）)])?([(（][上中下][）)])?[:：]')
# 当前行仅为文号
re_file_number3 = re.compile(r'^总?第\d+号$|[【\[(〔]2018[〕)\]】]第\d+号|^[12]\d{3}年第\d+号总期?第\d+号$')  # 北京的审计公告，总文号回单独作为一行
# 地区名单
re_regions_list = re.compile(r'^([\u4E00-\u9FA5]{0,10}[省市区县]([(（].*?流域[）)])*、)+([\u4E00-\u9FA5]{0,10}[省市区县]?)?$|[\u4E00-\u9FA5]{0,10}[省市区县]([(（].*?流域[）)])*$')
# 人名
# 广东省审计厅党组书记、厅长卢荣春
re_person_name = re.compile(r'审计[署厅局][\u4E00-\u9FA5、]*?(署长|厅长|局长|巡视员|长|党组书记)[\u4E00-\u9FA5]{2,5}$')
# 机构名
re_organization = re.compile(r'审计[局厅]$|部门$|院$|[银分]行$|中心$|部$|政府$')
# 发现空格
re_blank = re.compile(r'\s')
# 错误的段落标题（没有序号）
re_error_section_title = re.compile(r'基本情况|审计发现的(主要)?问题')

# <-------审计报告分类开始-------->
audit_q_str = r'、((跟踪|专项|)审计|[调检]查|审计[调检]查)?中?(发现|查出|存在|查明|指出)的?(主要|)问题([和及的]|整改情况$|$)'
re_base_case = re.compile(audit_q_str)  # 由于另外两种情况属于个例，暂时不考虑
# 该方法由于涉及规则较宽，仅可用于最后一项分类
re_base_case2 = re.compile(r'审计(.*?情况|意见|评价|建议|结果|.*?问题)|整改情况|情况$|问题$')
re_base_case3 = re.compile(r'不够?(规范|佳|到位|符合?|在岗|正?当|合格|合规|严格?|齐全'
                           r'|完整|准确|均衡|充分|及时|统一|实|彻底)'
                           r'|(开支|来源)不明|达不到|账务不清')  # "不"字相关的问题
re_yszx = re.compile(r'预算执行情?况?|其他财政收支')  # 从标题判断对否为预算执行
re_yszx_3 = re.compile(r'、基本情况$')
re_yszx_4 = re.compile(r'审计情况$')
re_qs_question = re.compile(r'问题$|方面$|案$')  # 全是审计问题的
re_case = re.compile(r'情况$|措施$')  # 全是审计情况的
re_waizi = re.compile(r'审计师意见\n|一、\s*审计师意见', re.DOTALL)  # 内容中包含审计师意见的
re_preface = re.compile(r'根据《中华人民共和国审计法》', re.DOTALL)  # 普通类型审计报告前言必备内容
# <-------审计报告分类结束-------->
# 数据清洗
re_sjs_content = re.compile(r'署[^名]')  # 判断当前的审计报告内容可能是审计署的（减少文本过滤的工作量）
# 青海省政府性债务审计结果答记者问
re_decoded = re.compile(r'解读|答记者问|的通知$|记者采访')
re_audit_key = re.compile(r'审计([^厅]|$)|整改|项目|财政收支|公告|报告|专项检查|检查结果|预算执行|政策措?施?落实|移送|银行贷款')  # 通过关键词判断是否为审计报告或整改报告
# 河南省审计厅审计结果公告办法（试行）
re_no_audit_key = re.compile(r'(实施方案|部门预算|的决定|名单|公示情况说明|公告办法)($|[(（].*?[）)])')
re_affix_table = re.compile(r'^\s*附表')  # 有些报告就只是一个表
# 信息抽取
num_str = r'[0-9○〇OО零一二三四五六七八九十]'
# re_date_str = r'(([%s年月日号截至到今明去初中末旬底第]|[上下]半|季度?)+(年|月|日|季度?)([%s年月日号截至到今明去初中末旬底第]|[上下]半|季度?)*)' % (num_str, num_str)
re_date_str = r'(([0-9○〇OО零一二三四五六七八九十年月日号截至到今明去初中末旬底第]|[上下]半|季度?)+(年|月|日|季度?)([0-9○〇○OО零一二三四五六七八九十年月日号截至到今明去初中末旬底第]|[上下]半|季度?)*)'
re_date = re.compile(re_date_str)
re_release_time1 = re.compile(r'(\d{4}年)第\d+[号期]公?告?([(（]总第\d+号[）)])?([(（][上中下][）)])?')
re_release_time2 = re.compile(r'[(（]([0-9○〇OО零一二三四五六七八九十年月日]+)\s*?公告[）)]')
re_release_time3 = re.compile(r'[(（](%s+年%s+月%s+日)\s*?公?告?[）)]' % (num_str, num_str, num_str))

re_section_column = re.compile(r'第(\d+)段')  # 段落列号

# 整改情况
re_zhenggai = re.compile(r'(落实|整改(检查)?|处理[\u4E00-\u9FA50-9]*?|执行(总体)?|查处)(工作)?情况|整改结果|纠正结果|整改工作报告')
re_audit = re.compile(r'审计(调查)?的?((工作)?报告|(结果|情况)?公告|(结果|情况)(公告)?)|'
                      r'检查结果|结果公告|情况审计|审签结果|'
                      r'预算执行[和及]其他财政(财务)?收支情况$|审计$|的报告$|信息公开报告$')  # 审计报告
re_project = re.compile(r'项目([零一二三四五六七八九十0-9]+期)?($|[a-zA-Z(（“"”])')


class ReQuestion(object):
    """有意义附件（认为内容包含审计问题或整改建议）"""
    def __init__(self):
        self.re1 = re.compile(r'审计[\u4E00-\u9FA50-9]*?问题$|'
                              r'整改效果较好的事例$|'
                              r'典型事例$|问题的具体情况$')  # 以下都是审计问题
        # 该规则存在一部分误判，但修改规则会导致更多的问题
        # 带来的问题是需要手动切分一部分数据（因为认为其是附件）
        #   + 但也存在不作为错误弹出的情况（段落标题不同），但可能性比较小
        # 切分后依然会在后面被当成附件抛出，手动重新加入即可
        self.re2 = re.compile(r'(审计|^)?(发现|查出)问题的?整改的?(建议|(有关)?情况)$')

    def search(self, string, *args, **kwargs):
        result1 = self.re1.search(string, *args, **kwargs)
        if result1 is not None:
            return result1
        result2 = self.re2.search(string, *args, **kwargs)
        if result2 is not None:
            return result2
        return None


class ReNoQuestion(object):
    """无意义附件（认为内容不包含审计问题或整改建议）"""
    def __init__(self):
        # 取得积极成效的典型事例
        # 国家质检总局落实审计决定和审计意见的情况
        # 人事部关于落实2003年审计意见整改情况的函
        # 中国工商银行关于落实审计建议加强内部整改情况的报告
        # 发现问题的整改情况
        # 删除了：.+落实(.+)的(情况|报告)$
        self.re_no_question = re.compile(r'(举措|措施)(和做法)?$|函$')  # 以下都不是审计问题

    def search(self, string, *args, **kwargs):
        return self.re_no_question.search(string, *args, **kwargs)


class ReSpetialTitle(object):
    """审计报告的附件，不应被单独作为审计报告处理的，但也分为有有效信息的和无有效信息的"""
    def __init__(self):
        self.re_spetial_titles = [
            ReNoQuestion(),  # 以下都不是审计问题
            ReQuestion(),  # 以下都是审计问题
        ]

    def search(self, string, *args, **kwargs):
        for each_re in self.re_spetial_titles:
            result = each_re.search(string, *args, **kwargs)
            if result is not None:
                return result
        return None


class RePageNumber(object):

    def __init__(self):
        self.re_page_number1 = re.compile(r'(^|\n)([—-]+\s*\d+\s*[—-]+)($|\n)', re.DOTALL)  # pdf页码
        self.re_page_number2 = re.compile(r'(^|\n)(·\s*\d+\s*·)($|\n)', re.DOTALL)  # pdf页码
        self.re_page_numbers = [
            self.re_page_number1, self.re_page_number2
        ]

    def sub(self, repl, string):
        for each_re in self.re_page_numbers:
            string = each_re.sub(repl, string)
        return string

    def search(self, *args, **kwargs):
        for each_re in self.re_page_numbers:
            result = each_re.search(*args, **kwargs)
            if result is not None:
                return result
        return None


class ReZhEnBlack(object):
    """pdf文件内容读取时，去除文中多余的空格，一般产生于数字和字母之间"""
    def __init__(self):
        """ 实际相当于处理了除英文与符号与英文之间的空格外的所有空格
        中中、中符、中数、中英
        符中、数中、英中
        [^a-zA-Z]: 中文和数字和符号
        [^0-9a-zA-Z]: 中文和符号
        注：此处修改处理单个空格为处理全部空格， \t也会被处理掉，所以表格不会再有表格结构
        """
        # 中/数/符-中/符
        self.re_zh_en_blank1 = re.compile(r'([^a-zA-Z])\s+([^0-9a-zA-Z])')
        # 中/符-中/数/符
        self.re_zh_en_blank2 = re.compile(r'([^0-9a-zA-Z])\s+([^a-zA-Z])')
        # 中-英
        self.re_zh_en_blank3 = re.compile(r'([\u4E00-\u9FA5])\s+([a-zA-Z])')
        # 英-中
        self.re_zh_en_blank4 = re.compile(r'([a-zA-Z])\s+([\u4E00-\u9FA5])')

    def _sub(self, repl, string):
        string = self.re_zh_en_blank1.sub(repl, string)
        string = self.re_zh_en_blank2.sub(repl, string)
        string = self.re_zh_en_blank3.sub(repl, string)
        return self.re_zh_en_blank4.sub(repl, string)

    def sub(self, rep1, string):
        return '\n'.join([self._sub(rep1, line) for line in string.split('\n')])


class ReTrash(object):
    """是否为非表或目录，即并不会研究对象的文件, 附件名做文件名的情况
    由于发现有文章目录变成超链接链接到文章的情况，因此在此过滤掉
    """
    def __init__(self):
        self.re_tu_table = re_tu_table
        self.re_catalog = re_catalog2

    def search(self, *args, **kwargs):
        result = self.re_tu_table.search(*args, **kwargs)
        if result is None:
            result = self.re_catalog.search(*args, **kwargs)
        return result


class ReSectionTitle(object):
    """识别一级标题"""
    def __init__(self, re_section_title):
        self.re_section_title = re_section_title

    def search(self, string, *args, **kwargs):
        title_1 = self.re_section_title.search(string, *args, **kwargs)
        # 带一级标题号且不是目录
        if title_1 is not None and re_catalog2.search(string, *args, **kwargs) is None:
            return title_1
        return None

    def findall(self, string, *args, **kwargs):
        """找到文章中所有的一级标题标号"""
        result = []
        for line in string.split('\n'):
            title_1 = self.re_section_title.search(line, *args, **kwargs)
            # 带一级标题号且不是目录
            if title_1 is not None and re_catalog2.search(line, *args, **kwargs) is None:
                result.append(title_1.groups())
        return result


class ReSectionTitle1(ReSectionTitle):
    """识别一级标题"""
    def __init__(self):
        re_section_title = re.compile(r'(^([一二三四五六七八九十零]+)\s*、(.*?[^\d])$)')  # 一级标题
        super(ReSectionTitle1, self).__init__(re_section_title)


class ReSectionTitle2(ReSectionTitle):
    """识别二级标题"""
    def __init__(self):
        re_section_title = re.compile(r'(^[（(]\s*([一二三四五六七八九十零]+)\s*[)）](.*?[^\d])$)')  # 二级标题
        super(ReSectionTitle2, self).__init__(re_section_title)


class ReSectionTitle3(ReSectionTitle):
    """识别数字段落标题"""
    def __init__(self):
        re_section_title = re.compile(r'(^(\d+)[.．、](.*?[\u4E00-\u9FA5]+.*?[^\d])$)')  # 数字段落标题
        super(ReSectionTitle3, self).__init__(re_section_title)


class ReSectionTitle4(ReSectionTitle):
    """识别数字段落标题"""
    def __init__(self):
        re_section_title = re.compile(r'(^[(（](\d+)[）)](.*?[\u4E00-\u9FA5]+.*?[^\d])$)')  # 数字段落标题
        super(ReSectionTitle4, self).__init__(re_section_title)


class ReDealTitle(object):
    """对标题提纯，有的标题里包含审计文号，有的标题是切分的附件等情况"""

    def __init__(self):
        re_deal_title1 = re.compile(r'[：:]\s*["“](.*?)["”]$')
        re_deal_title2 = re.compile(r'[：:]\s*(.*?)$')
        re_deal_title3 = re.compile(r'^《(.+)》$')

        self.re_deal_title_end = re.compile(r'^(.+)$')  # 最终规则都没通过就认为标题没问题
        self.re_rules = [
            re_deal_title1,
            re_deal_title2,
            re_deal_title3,
        ]
        # 围绕中心 把握立意 写出特色——谈2003年中央预算执行审计“两个报告”的特点
        self.re_deal_title4 = re.compile(r'^(.+)——')
        # 虹桥综合交通枢纽仙霞西路(可乐路——协和路)道路新建工程项目竣工决算审计结果
        # 2017年度上海市城市排水有限公司世界银行贷款白龙港片区南线输送干线完善工程——过江管及连接管工程(上海城市环境治理APL三期项目子项目)执行情况审计结果
        self.re_deal_title5 = re.compile(r'[(（].+——.+[）)]|审计结果$')  # 排除特殊情况

    def _search(self, string, *args, **kwargs):
        for each_rule in self.re_rules:
            result = each_rule.search(string, *args, **kwargs)
            if result is not None:
                return result.groups()[0]
        return string

    def search(self, string, *args, **kwargs):
        result = self._search(string, *args, **kwargs)
        result2 = self.re_deal_title4.search(result)
        if result2 is not None and self.re_deal_title5.search(result) is None:
            return result2
        return self.re_deal_title_end.search(result, *args, **kwargs)


class ReDealTitle2(ReDealTitle):
    """可以识别标题前后缀的标题提纯模块，并可以去除标签前后的特殊字符"""
    def __init__(self):
        super(ReDealTitle2, self).__init__()
        re_spetial_title1 = re.compile(r'^“([^”]+)$')
        re_spetial_title2 = re.compile(r'^(.+)[（(]$')
        re_spetial_title3 = re.compile(r'^\d{4}年第\d+号公?告?[:：](.+)$')
        # 山东省审计厅审计结果公告2004年第02号
        re_spetial_title4 = re.compile(r'(.+)\d{4}年第\d+号公?告?$')

        self.re_suffix = re.compile(r'^(.+)([(（].+[）)])$')
        self.re_prefix = re.compile(r'^(【.+】)(.+)$')
        self.re_spetial_title = re.compile(r'^[^a-zA-Z_\u4E00-\u9FA5]|[^0-9a-zA-Z_\u4E00-\u9FA5]$')
        self.re_spetial_titles = [
            re_spetial_title1, re_spetial_title2, re_spetial_title3, re_spetial_title4
        ]

    def _search(self, string, *args, **kwargs):
        string = super(ReDealTitle2, self)._search(string, *args, **kwargs)
        # 有些不是特殊字符的也要处理
        # if self.re_spetial_title.search(string, *args, **kwargs):
        # print('原：', string)
        for each_re in self.re_spetial_titles:
            result = each_re.search(string, *args, **kwargs)
            if result is not None:
                string = result.groups()[0]
        # print('改：', string)
        return string

    def search2(self, string, *args, **kwargs):
        prefix, suffix = None, None
        string = self.search(string, *args, **kwargs).groups()[0]
        if self.re_spetial_title.search(string, *args, **kwargs):
            result1 = self.re_prefix.search(string, *args, **kwargs)
            if result1 is not None:
                prefix, string = result1.groups()
            result2 = self.re_suffix.search(string, *args, **kwargs)
            if result2 is not None:
                string, suffix = result2.groups()
        return prefix, string, suffix


re_spetial_title = ReSpetialTitle()
re_no_question = ReNoQuestion()  # 以下都不是审计问题
re_question = ReQuestion()  # 以下都是审计问题

re_page_number = RePageNumber()
re_frash = ReTrash()  # 识别并非正常需要的审计报告的附件
re_zh_en_blank = ReZhEnBlack()  # pdf文件内容读取时，去除文中多余的空格
# 新增规则[^\d]$,标题不能以数字结尾
re_section_title_1 = ReSectionTitle1()
re_section_title_2 = ReSectionTitle2()
re_section_title_3 = ReSectionTitle3()
re_section_title_4 = ReSectionTitle4()
re_deal_title = ReDealTitle2()  # 对标题提纯，有的标题里包含审计文号，有的标题是切分的附件等情况


if __name__ == '__main__':
    print(re_file3.search('中央部门预算执行审计发现问题的整改情况.rar').group())
    print(re_file2.search('中央部门预算执行审计发现问题的整改情况.rar'))
    print(re_frash.search('中央部门预算执行审计发现问题的整改情况.rar'))
    print(re_section_title_1.search('一、审计发现的问题').groups())
    print(re_section_title_1.findall('一、审计发现的问题'))
    print(re_deal_title.search('关于2007年度中央预算执行和其他财政收支的审计工作报告——2008年8月27日在第十一届全国人民代表大会常务委员会第四次会议上').groups()[0])
    print(re_deal_title.search('《关于2007年度中央预算执行和其他财政收支的审计工作报告——2008年8月27日在第十一届全国人民代表大会常务委员会第四次会议上》').groups()[0])
    print(re_deal_title.search('虹桥综合交通枢纽仙霞西路(可乐路——协和路)道路新建工程项目竣工决算审计结果').groups()[0])
    print(re_page_number.search('aaa\n2010-05-20\n'))
    print(re_page_number.search('aaa\n-05-\n'))
    print(re_page_number.search('aaa\n- 05 -\n'))
    print(re_page_number.search('-- 5--\n'))
    print(re_page_number.search('aaa\n·05·'))
    print(re_page_number.search('·78·\n世界银行贷款云南职业技术教育与培训项目2017年度公证审计结果').groups())
    print([re_page_number.sub(r'\1\3', '·78·\n世界银行贷款云南职业技术教育与培训项目2017年度公证审计结果')])

