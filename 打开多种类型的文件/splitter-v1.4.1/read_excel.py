import pandas as pd
from splitter.base.models import FileDatabase, TableData


__all__ = ['ReadExcel']


class ReadExcel(FileDatabase):
    """读取Word内容，目前仅读取文本内容和表格"""
    def __init__(self, data_xls, header=None, *args, **kwargs):
        super(ReadExcel, self).__init__()
        for sheet_name in data_xls.sheet_names:
            df = data_xls.parse(sheet_name=sheet_name, header=header, *args, **kwargs)
            table = [[word if pd.notnull(word) else None for word in line] for line in df.values]
            self.add(TableData(table))

    @classmethod
    def open(cls, file_path: str, header=None, *args, **kwargs):
        data_xls = pd.ExcelFile(file_path)
        return cls(data_xls, header=header, *args, **kwargs)


if __name__ == '__main__':
    read_e = ReadExcel.open("D:/job/审计公告/信息抽取全项目/表格提取/表格中的机构信息提取/table2words/ceshi/aaa.xlsx")
    for table in read_e.get_table():
        table.find_title()
        table.set_head()
        print(table.title)
        print(table.head)
        print(table.table)
