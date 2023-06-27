import re
import decimal

from pdfplumber.utils import DEFAULT_X_TOLERANCE
from pdfplumber.utils import DEFAULT_Y_TOLERANCE
from pdfplumber.utils import to_list
from pdfplumber.utils import cluster_objects
from pdfplumber.utils import collate_line


re_catalog = re.compile(r'[\-.。•]{7,}|[…]{3,}')  # 识别目录，文章分类用
re_end_punctuation = re.compile(r'[.。？?!！:：]$')  # 冒号也可能使段落的结束符


def extract_text(chars,
                 x_tolerance=DEFAULT_X_TOLERANCE,
                 y_tolerance=DEFAULT_Y_TOLERANCE):

    if len(chars) == 0:
        return None

    chars = to_list(chars)
    doctop_clusters = cluster_objects(chars, "doctop", y_tolerance)

    # 有的页面没有一行到头的数据，则默认为500（实际一般为534）
    lines, begin_x0, end_x1 = [], decimal.Decimal(0), decimal.Decimal(500)
    for line_chars in doctop_clusters:
        line = collate_line(line_chars, x_tolerance)
        # print([line])
        begin_char, end_char = line_chars[0], line_chars[-1]
        for char in line_chars:
            # print(char)
            if char['x0'] < begin_char['x0']:
                begin_char = char
            if char['x1'] > end_char['x1']:
                end_char = char
        # print(begin_char['x0'], end_char['x1'], end_char['x1'] - begin_char['x0'])
        lines.append((line, begin_char['x0'], end_char['x1'], (end_char['x1']-begin_char['x0'])/len(line_chars),
                      abs(max(i['y1'] for i in line_chars) - min(i['y0'] for i in line_chars))))
        if begin_char['x0'] < begin_x0:
            begin_x0 = begin_char['x0']
        if end_char['x1'] > end_x1:
            end_x1 = end_char['x1']

    # 去除页码
    # re_page_num = re.compile(r'^[—\-]*\s*\d+\s*[—\-]*$')
    # if re_page_num.search(lines[-1][0].strip()) is not None:
    #     lines = lines[:-1]
    # print('begin_x0, end_x1: ', begin_x0, end_x1)
    paragraphs, end_null = [""], True  # 自动识别分段，而非每行后都加回车
    before_row_hight = lines[0][-1]
    for line, line_begin, line_end, char_size, row_hight in lines:
        # print(line)
        # begin = line_begin - begin_x0
        # reteact = round(begin/char_size)  # 四舍五入保留整数作为缩进字符数
        # line = "  " * reteact + line  # 缩进一个字符即加两个空格
        # if reteact >= 2:  # 首行缩进大于两字符的认为是新段
        #     paragraphs.append(line)
        # print(abs(before_row_hight - row_hight), [line])

        if line.strip() == '':
            paragraphs.append(line)
            paragraphs.append("")
            end_null = True
        # 句尾存在超过一个字符长度的空位，认为可能是新段
        # elif end_x1 - line_end > char_size and (end_x1 - line_end > char_size * 2 or re_end_punctuation.search(line)):
        elif end_x1 - line_end > char_size * 2 or re_end_punctuation.search(line.rstrip()):
            # 如果有两个字符的空位，或者句子结束符结尾（去除结尾空格后），认为是新段
            # print(end_x1 - line_end, end_x1, line_end, char_size, [line])
            paragraphs[-1] += line
            paragraphs.append("")
            end_null = True
        elif abs(before_row_hight - row_hight) > 10:  # 行高不同，认为是新行
            # print('aaa', before_row_hight, row_hight)
            paragraphs.append("")
            paragraphs[-1] += line
            end_null = True
        elif re_catalog.search(line) is not None:
            # 目录单独为一行，不与其他内容同行
            if end_null:
                paragraphs[-1] += line
            else:
                paragraphs.append(line)
            paragraphs.append("")
            end_null = True
        else:  # 不是新段的句加入当前最后一段中
            paragraphs[-1] += line
            end_null = False
        before_row_hight = row_hight
    if end_null:
        paragraphs = paragraphs[:-1]

    coll = "\n".join(paragraphs)
    return coll
