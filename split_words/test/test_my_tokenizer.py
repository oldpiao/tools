import re
import jieba.posseg as peg

from split_words.segmente import POSWords
from split_words.segmente import MyRe, MyTagRe
from split_words.segmente.my_tag_re.rule import SplitRules
from split_words import settings


def test_my_re():
    my_re = MyRe()
    my_re.load_dict(settings.RE_DICT)
    my_re.add_word('你好哈{0,2}', None, 'v')
    results = my_re.findall('你好哈哈哈')
    my_re.del_word('你好哈{0,2}')
    for i in my_re.rules.items():
        print(i)
    print(results)


def test_my_tag_re():
    sentence = '你们看中华人民共和国国旗随风飘扬在天上非常美丽s壮观我好喜欢'
    words = POSWords(peg.cut(sentence))
    assert words.word2str() == '你们/r/看/v/中华人民共和国/ns/国旗/n/随风飘扬/i/在/p/天上/s/非常/d/美丽/ns/s/x/壮观/a/我/r/好/a/喜欢/v'
    my_tag_re = MyTagRe()
    my_tag_re.load_dict('test_dict/tag_re_dict_test.txt')
    words.words = my_tag_re.cut(words.words)
    print(words.word2str())
    assert words.word2str() == '你们/r/看/v/中华人民共和国国旗/n/随风飘扬在天上/x/非常美丽s壮观/x/我/r/好/a/喜欢/v'


def test_my_tag_re2():
    rule_list = SplitRules('a/你/_/-/-a/_a/_nx')
    assert len(rule_list.split_rule) == 7
    assert rule_list.split_rule[0].rule_len is None and rule_list.split_rule[0].rule == 'a'
    assert rule_list.split_rule[1].rule == '你' and rule_list.split_rule[1].__class__.__name__ == 'Mean'
    assert rule_list.split_rule[2].rule == '_' and rule_list.split_rule[2].__class__.__name__ == 'Mean'
    assert rule_list.split_rule[3].rule == '-' and rule_list.split_rule[3].__class__.__name__ == 'Mean'
    assert rule_list.split_rule[4].rule == 'a' and rule_list.split_rule[4].__class__.__name__ == 'Mean'
    assert rule_list.split_rule[5].rule_len == 1 and rule_list.split_rule[5].rule == 'a'
    assert rule_list.split_rule[6].rule_len == 2 and rule_list.split_rule[6].rule == 'nx'


def test_my_tag_re3():
    words = POSWords(peg.cut('今天2016年12月15日晴'))
    words.my_tag_re.add_word('m+')
    words.tag_re_cut()
    print(words.word2str())
    assert words.word2str2() == '今天/2016年12月15日/晴'


def deal_way(word):
    new_word = re.search(r'\d+年\d+月\d+日', word)
    if new_word is not None:
        return new_word.group()
    else:
        return word


def test_my_tag_re4():
    words = POSWords(peg.cut('我你他你我你我你你你你今天2016年12月15日晴'))
    words.my_tag_re.add_word('你+/今天/m*/v*')
    words.tag_re_cut()
    print(words.word2str())
    assert words.word2str2() == '我/你/他/你/我/你/我/你你你你今天2016年12月15日晴'
    words = words.deal_word(deal_way)
    assert words.word2str2() == '我/你/他/你/我/你/我/2016年12月15日'
    print(set(words.words))


def test_my_tag_re5():
    words = POSWords(peg.cut('未及时披露公司重大事项,未依法履行其他职责经查明,海虹企业(控股)股份'
                              '有限公司(以下简称“海虹控股”)存在以下违规行为:2011年4月10日,海虹控'
                              '股全资子公司SinoPowerManagementLimited(以下简称“SinoPower”)与梅朝'
                              '辉签订协议,协议约定SinoPower以9,000万港元购买梅朝辉持有的香港上市公'
                              '司首长科技集团有限公司(股份名称:首长科技,股份代码:00521)2亿股可换股'
                              '票据,同时约定在2011年9月16日前,梅朝辉或其指定第三方回购上述可换股票'
                              '据,若梅朝辉或其指定第三方未能上述履行回购义务,SinoPower有权要求梅朝'
                              '辉赔偿违约金2,000万港元.     在上述期限内,梅朝辉或其指定第三方未能履'
                              '行上述回购义务,2011年12月,SinoPower收到梅朝辉违约金2,000万港元并计入'
                              '营业外收入,上述违约金收入约占海虹控股2010年经审计净利润的137%.对于前'
                              '述事项,海虹控股未履行临时信息披露义务.海虹控股的上述行为违反了本所《'
                              '股票上市规则(2008年修订)》第2.1条,第9.2条的规定.海虹控股的董事长贾岩'
                              '燕,总裁康健未能恪尽职守,履行诚信勤勉义务,违反了本所《股票上市规则(2'
                              '008年修订)》第1.4条,第3.1.5条的规定,对海虹控股上述违规行为负有重要责'
                              '任.     海虹控股的董事会秘书上官永强未能恪尽职守,履行诚信勤勉义务,违'
                              '反了本所《股票上市规则(2008年修订)》第1.4条,第3.1.5条,第3.2.2条的规定'
                              ',对海虹控股上述违规行为负有重要责任.'))
    # words = POSWords(peg.cut('未及时披露公司重大事项一,《行政处罚决定书》的主要内容经查,2013年,2014年公司与公司第一大股东东莞勤上集团有限公司(以下简称“勤上集团”)存在非经营性资金往来情况,累计金额为182,750万元.公司对该事项未履行信息披露义务.违反了《证券法》第63条,第65条,第67条的规定.'))
    print(words.word2str())
    words.my_tag_re.load_dict(settings.TAG_RE_DICT)
    words.tag_re_cut()
    print(words.word2str())


def test_my_tag_re6():
    words = POSWords(peg.cut('你1,000,200.2332'))
    print(words.word2str())
    # words.my_tag_re.add_word('.+', freq=None, tag='ni')
    words.my_tag_re.add_word('\d/,/m/x/\d', freq=None, tag='mm')
    words.my_tag_re.add_word('\d/,/m', freq=None, tag='mm')
    words.tag_re_cut()
    print(words.word2str())
    # assert words.word2str2() == '我/你/他/你/我/你/我/你你你你今天2016年12月15日晴'
    # words.deal_word(deal_way)
    # assert words.word2str2() == '我/你/他/你/我/你/我/2016年12月15日'
    # print(set(words.words))


def test_my_tag_re7():
    rules = [
        '你*/你们/看看+/我{1,3}',
        '你*/你们/看看+/我{3}',
        'r*/v+/r{1,3}',
        'r*/v+/r{1,}'
    ]
    words = POSWords(peg.cut('你你你们看看看看看看我我我我好好好好好好开心'))
    print(words.word2str())  # .*?
    for rule in rules:
        new_word, wn = SplitRules(rule).match(words.words)
        print(new_word, wn)


def test_my_tag_re8():
    """测试新版规则，支持.*+?{n}{m,n}{m,}"""
    words = POSWords(peg.cut('你你你你你你你你你你'))
    print(words.word2str())  # .*?
    rules = [
        '你*/你+/你*/你/你+',
        '你?',
        '你+?',
        '你*?',
        '你{2,4}',
        '你{3,5}?',
        '你{4,}?',
    ]
    for rule in rules:
        rule_list = SplitRules(rule)
        new_word, wn = rule_list.match(words.words, default_tag='x')
        print(new_word, wn)


def test_jieba():
    ts = peg.POSTokenizer()
    ts.tokenizer.load_userdict('test_dict/use_dict_test.txt')
    ts.tokenizer.add_word('国旗，随风飘扬', tag='vv')
    print(ts.user_word_tag_tab)
    words = POSWords(ts.cut('你们看中华人民共和国国旗，随风飘扬在天上非常美丽s壮观我好喜欢\r\n\taaa\rs是多少  \r\sdsd 是 多   少'))
    print([words.word2str()])


if __name__ == '__main__':
    # 中华人民共和国/ns/国旗/n/随风飘扬/i/在/p/天上/s
    # test_my_re()
    # test_my_tag_re()
    # test_my_tag_re2()
    # test_my_tag_re3()
    # test_my_tag_re4()
    # test_my_tag_re5()
    # test_my_tag_re6()
    # test_my_tag_re7()
    # test_my_tag_re8()
    test_jieba()
