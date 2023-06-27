import sys
import os
import json
import logging
import time
from copy import deepcopy

from tqdm import tqdm
import pandas as pd
import xlwings as xw

cur_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.abspath(os.path.join(cur_dir, ".."))
sys.path.append(base_dir)


class OpenExcel(object):
    """在excel中做数据标注
    标注流程：
        设置要标注的sheet页，设置原文内容列、标注信息列，设置
    """
    def __init__(self, f_path):
        self.app = xw.App(visible=False, add_book=False)
        self.wb = self.app.books.open(f_path)

    def num2col_num(self, num: int):
        begin = ord("A")
        col_num = ""
        while num > 0:
            n = num % 26
            num = num // 26
            col_num += chr(begin + (n - 1))
        return col_num

    def add_sheet(self, data, sheet_name, before=None, after=None):
        while True:
            if any([sheet_name == sht.name for sht in self.wb.sheets]):
                sheet_name = sheet_name + "_1"
                logging.warning("sheet页已存在，修改sheet页名为：{}".format(sheet_name))
            else:
                break
        self.wb.sheets.add(name=sheet_name, before=before, after=after)
        sht = self.wb.sheets(sheet_name)
        row_num, col_num = len(data), len(data[0])
        for i in range(col_num):
            col_num_str = self.num2col_num(col_num + 1)
            for j in range(row_num):
                cell = sht.range("{}{}".format(col_num_str, j + 1))
                cell.raw_value = data[j][i]

    def __del__(self):
        self.wb.save()
        self.wb.close()
        self.app.quit()
        print("保存修改，关闭文件，关闭APP。。。")


def run(f_path, cols=None, sheet_name=None):
    oe = OpenExcel(f_path)
    if sheet_name is None:
        sheet_name = oe.wb.sheets[0].name
    sht = oe.wb.sheets(sheet_name)
    row_num, col_num = sht.used_range.shape
    if cols is None:
        cols = [oe.num2col_num(i) for i in range(1, col_num+1)]
    for n, i in enumerate(cols):
        if isinstance(i, int):
            cols[n] = oe.num2col_num(i)
    for col in cols:
        for row in range(1, row_num+1):
            key = "{}{}".format(col, row)
            cell = sht.range(key)
            if isinstance(cell.raw_value, str):
                if cell.raw_value.strip() != cell.raw_value:
                    print("{}{}-->{}".format(key, [cell.raw_value], [cell.raw_value.strip()]))
                    cell.raw_value = cell.raw_value.strip()


if __name__ == '__main__':
    file_path = os.path.join(cur_dir, "data/机构职责关系构建mock数据/001-《郑州市防汛应急预案》4月20日-关系.xlsx")
    run(file_path, cols=list("ABCDEFG"))
