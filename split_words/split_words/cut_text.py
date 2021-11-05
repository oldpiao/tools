# 对文本进行预处理，将其切分成短句再处理
# 由于目标词可能存在考虑符号的情况，此时应该控制是否需要将所有符号都切开
# 切分后可以多进程并行处理，提高速率
from split_words.utils import ReCutSentence, ReClause, CutSpetialNumber


re_cut_sentence = ReCutSentence()  # 切分句
re_clause = ReClause()  # 切分子句


__all__ = ['cut_spetial_number', 'cut_sentence', 'cut_clause']


cut_spetial_number = CutSpetialNumber.init  # 切分出用逗号分开的数字


def cut_sentence(document):
    """将文本分句
    用于预测数据处理，使用时建议与识别段落序号的功能一块使用，将段落标题序号去除，
    因为段落标题序号会对结果产生影响
    例：三、审计处理情况及意见	0.462853104	“三同时”制度执行情况

    from article_tree.chaper_classifier.judge_chaper import is_chapter
    sentence = is_chapter.is_chapter(sentence).del_num(sentence)
    """
    for sentence in re_cut_sentence.split(document):
        yield sentence


def cut_clause(sentence):
    """将句子切分为子句，使用逗号等分隔开的句子，防止跨句提词
    特殊情况处理：
        + 数字中间有逗号：12,345,678、12,345,678
    """
    sentences = cut_spetial_number(sentence)
    spetial_numbers = sentences.get_spetial_number()
    clauses = sentences.get_clauses()
    ws = []
    ws.extend(re_clause.findall(clauses[0]))
    for n, i in enumerate(clauses[1:], 0):
        ss = re_clause.findall(i)
        ws[-1] = ws[-1] + spetial_numbers[n] + ss[0]
        if len(ss) > 1:
            ws.extend(ss[1:])
    return ws
