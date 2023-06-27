import sys
import os
# import collections
import pandas as pd

cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cur_dir, ".."))

from article_tree import FindChapter


def txt2dataframe(text):
    fc = FindChapter.open_str(text)
    res = fc.to_dict()
    lines = []
    title = []
    for line_type, line in zip(res["data"]["line_types"], res["data"]["lines"]):
        line = "".join(line)
        if line_type == -1:
            lines.append(["-".join(title), line])
        elif len(line) > 50:
            lines.append(["-".join(title[:line_type]), line])
        else:
            title = title[:line_type]
            if len(title) < line_type:
                title.extend(["" for _ in range(line_type - len(title))])
            title.append(line)
            print(line_type, title)
            # lines.append(["-".join(title), ""])
    df = pd.DataFrame(lines, columns=["标题", "内容"])
    return df


def run():
    f_path = os.path.join(cur_dir, "../data/深圳市宝安区突发事件总体应急预案.docx.txt")
    save_path = os.path.join(cur_dir, "../data/深圳市宝安区突发事件总体应急预案.xlsx")
    with open(f_path, "r", encoding="utf-8") as f:
        data = f.read()
    df = txt2dataframe(data)
    df.to_excel(save_path, header=True, index=False)


if __name__ == '__main__':
    run()
