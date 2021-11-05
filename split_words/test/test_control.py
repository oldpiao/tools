from split_words.control.splitword_flow1 import splitword_flow as splitword_flow1
from split_words.control.splitword_flow2 import splitword_flow as splitword_flow2
from split_words.control.splitword_flow3 import splitword_flow as splitword_flow3


def test_splitword_flow():
    sentence = '你们看中华人民共和国国旗随风飘扬在天上非常美丽s壮观我好喜欢《我是一本书》啊啊啊《我是一条法规》'
    print(splitword_flow1(sentence).word2str())
    print(splitword_flow2(sentence).word2str2())
    print(splitword_flow3(sentence).word2str2())


if __name__ == '__main__':
    test_splitword_flow()
