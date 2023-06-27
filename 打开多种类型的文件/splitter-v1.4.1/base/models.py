# 将各类型文本转换成Python对象的基类方法，之后依据该基类实现不同文本类型的子类
import re

import pandas as pd


__all__ = ['TextData', 'TableData', 'FileDatabase']


class DataBases(object):

    def __init__(self, page=None, type_='base'):
        self.type_ = type_
        self.page = page

    def to_save(self):
        return {
            "type": self.type_,
            "data": {
                "page": self.page
            }
        }


class TextData(DataBases):
    """文本对象，记录文本的一个段落的文本信息"""
    def __init__(self, data="", page=None, paragraph_style="Normal"):
        """
        :param data:
        :param page:
        :param paragraph_style: 段落类型（应该是大纲结构）
            ["Normal", "Heading 1, "Heading 2", ...]
        """
        super(TextData, self).__init__(page=page, type_='text')
        self.data = data
        self.paragraph_style = paragraph_style

    def str(self):
        return self.data

    def add(self, data: str):
        self.data += data
        return self

    def to_save(self):
        result = super(TextData, self).to_save()
        result['data'].update({
            "data": self.data,
        })
        return result

    def to_word(self, document):
        document.add_paragraph(self.data)
        return document


class TableData(DataBases):
    """表格对象，用于记录文本的一个表格信息"""
    def __init__(self, table=None, title=None, topnote=None, endnote=None, head=None, page=None):
        super(TableData, self).__init__(page=page, type_='table')
        if table is None:
            self.table = []
        else:
            self.table = table
        self.title = title  # 表格标题
        self.topnote = topnote  # 表格中标题后表格前的注释内容
        self.endnote = endnote  # 表格尾注
        self.head = head

    def str(self):
        return self.table

    def del_null_line(self):
        """删除空行"""
        table = []
        for line in self.table:
            no_null_line = [cell for cell in line if cell is not None]
            if len(no_null_line) != 0:
                table.append(line)
        self.table = table

    def find_title(self):
        """认为开头为仅有一列内容即为标题"""
        title = []
        for n, line in enumerate(self.table):
            no_null_line = [cell for cell in line if cell is not None]
            if len(no_null_line) == 1:
                title.append(no_null_line[0])
            else:
                if len(title) != 0:
                    self.table = self.table[n:]
                    self.title = '\n'.join(title)
                break
        return self.title

    def set_head(self, header=0):
        """
        设置表格的头
        :param header: 默认为0，代表第0行，如果不为第0行，则之前的行会被删除
        :return:
        """
        self.head = self.table[header]
        self.table = self.table[header+1:]

    def add(self, table: list):
        self.table.extend(table)
        return self

    def add_line(self, line):
        self.table.append(line)
        return self

    def read_pd(self):
        return pd.DataFrame(self.table)

    def to_save(self):
        result = super(TableData, self).to_save()
        result['data'].update({
            "table": self.table,
            "title": self.title,
            "topnote": self.topnote,
            "endnote": self.endnote,
            "head": self.head,
        })
        return result

    def to_word(self, document):
        if self.table == list():
            return document
        table = document.add_table(rows=0, cols=len(self.table[0]))  # 插入表格
        table.style = 'Table Grid'
        for line in self.table:
            row_cells = table.add_row().cells
            for n, column in enumerate(line, 0):
                if column is None:
                    column = ''
                row_cells[n].text = str(column)
        return document


data_type = (TextData, TableData)  # 文本或表格对象，用于判断对象类型


class TextPreprocess(object):
    """处理文本中的特殊字符，将文本内容转化为更好处理的格式"""
    def __init__(self, sprtial_code=True, stop_null=True, strip=True, n_blank=0):
        self.sprtial_codes = ['\xa0', '\u3000']
        self.n_blank = n_blank
        if n_blank != 0:
            self.deal_sprtial_codes = self._deal_blank2enter
        if sprtial_code:
            self.deal_sprtial_codes = self._deal_sprtial_codes
        else:
            self.deal_sprtial_codes = self.default
        if stop_null:
            self.deal_stop_null = self._deal_stop_null
        else:
            self.deal_stop_null = lambda x: False
        if strip:
            self.deal_strip = self._deal_strip
        else:
            self.deal_strip = self.default

    def _deal_blank2enter(self, data, re_with='\n'):
        """将两个连续的空格转换成回车"""
        data = self._deal_sprtial_codes(data)
        return re.sub(r'\s{%s}' % self.n_blank, re_with, data)

    def _deal_sprtial_codes(self, data, re_with1='\n', re_with2=' '):
        """将连续的特殊空格换成回车，将单个特殊空格转化成普通空格"""
        for code in self.sprtial_codes:
            data = data.replace(code*2, re_with1)
        for code in self.sprtial_codes:
            data = data.replace(code, re_with2)
        # data = re.sub(r'\n', r'\\n', data)
        # data = re.sub(r'\s', r' ', data)
        # data = re.sub(r'\\n', r'\n', data)
        return data

    def _deal_stop_null(self, data):
        return data == ""

    def _deal_strip(self, data):
        return data.strip()

    def default(self, data):
        return data


class SubCharRules(object):

    def and28(self, string):
        """
        将"& "转换成"8,"，
        将"&"转换成"8."，
        """
        string = re.sub(r'& ', r"8,", string)
        string = re.sub(r'&', r"8.", string)
        return string


class FileDatabase(SubCharRules):
    """文本对象的基类，将PDF、word等类型文件转换成相同格式的Python对象，统一接口，用于之后的处理"""
    def __init__(self):
        self.doc = []

    def sub_spetial_char(self, func):
        """
        替换文本中的特殊字符，将其转换成长正常字符
        :param func: DealRules的方法
        """
        for child in self.doc:
            if isinstance(child, TextData):
                child.data = func(child.data)
            if isinstance(child, TableData):
                table = []
                for rows in child.table:
                    line = []
                    for cell in rows:
                        if cell is None:
                            line.append(cell)
                        else:
                            line.append(func(cell))
                    table.append(line)
                child.table = table

    def text_preprocess(self, sprtial_code=True, stop_null=True, strip=True, n_blank=0):
        """处理文本中的特殊字符，将文本内容转化为更好处理的格式"""
        tp = TextPreprocess(sprtial_code, stop_null, strip, n_blank)
        new_doc = []
        for data in self.doc:
            if isinstance(data, TextData):
                data.data = tp.deal_sprtial_codes(data.data)
                for new_data in data.data.split('\n'):
                    new_data = tp.deal_strip(new_data)
                    if tp.deal_stop_null(new_data):
                        continue
                    else:
                        new_doc.append(TextData(new_data))
            else:
                new_doc.append(data)
        self.doc = new_doc
        return self

    def close(self):
        pass

    def add(self, data: data_type):
        self.doc.append(data)
        return self

    def extend(self, datas: list):
        for data in datas:
            self.add(data)
        return self

    def get_text(self):
        """获取全部文本对象"""
        return [text for text in self.doc if isinstance(text, TextData)]

    def get_text_strs(self):
        """获取全部文本对象"""
        return "\n".join([text.data for text in self.get_text()])

    def get_table(self):
        """获取全部表格对象"""
        return [table for table in self.doc if isinstance(table, TableData)]

    def get_all_strs(self, table_none=''):
        """
        将表格转化成行与文本内容一块输出
        表格输出成一行，单元格中间用\t隔开行之间用\t\t隔开
        :param table_none: 表格中无内容的格默认用空字符代替
        :return:
        """
        contents = []
        for table_or_txt in self.doc:
            if isinstance(table_or_txt, TableData) and table_or_txt.table != []:
                lines = []
                for line in table_or_txt.table:
                    new_line = []
                    for word in line:
                        if word is None:
                            new_line.append(table_none)
                        else:
                            new_line.append(word)
                    lines.append("\t".join(new_line))
                contents.append("\t\t".join(lines))
            elif isinstance(table_or_txt, TextData):
                contents.append(table_or_txt.data)
        return "\n".join(contents)

    def get_all_strs2(self, table_none=''):
        """
        将表格转化成行与文本内容一块输出
        表格按行输出，中间用\t隔开
        :param table_none: 表格中无内容的格默认用空字符代替
        :return:
        """
        contents = []
        for table_or_txt in self.doc:
            if isinstance(table_or_txt, TableData) and table_or_txt.table != []:
                for line in table_or_txt.table:
                    new_line = []
                    for word in line:
                        if word is None:
                            new_line.append(table_none)
                        else:
                            new_line.append(word)
                    contents.append("\t".join(new_line))
            elif isinstance(table_or_txt, TextData):
                contents.append(table_or_txt.data)
        return "\n".join(contents)

    def deal_table(self):
        """
        处理表格，合并因分页而拆分开的表，在表附近的文本中寻找表信息
        该功能待完善，功能设计较可以在table_perfect中的实现，再在此处调用
        """
        from splitter.base.table_perfect import TablePerfect
        a = TablePerfect(self)
        return self

    def to_save(self):
        """用于数据固化，将对象中的信息以字典的形式返回，合并成一个列表返回，之后可以将其保存成json文件"""
        return list([data.to_save() for data in self.doc])

    def read_json(self, doc: list):
        """将固化的数据重新读入内存"""
        for data in doc:
            if data['type'] == "text":
                self.add(TextData(**data['data']))
            elif data['type'] == "table":
                self.add(TableData(**data['data']))
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def ceshi():
    fd = FileDatabase()
    fd.add(TextData().add("aaaa"))
    fd.add(TableData().add([[1, 2, 3], [1, 2, 3], [1, 2, 3]]))
    fd.add(TextData().add("aaaa"))
    fd.add(TextData().add("aaaa"))
    fd.add(TableData().add([[1, 2, 3], [1, 2, 3], [1, 2, 3]]))
    fd.add(TextData().add("aaaa"))
    print(list(fd.to_save()))
    fd2 = FileDatabase().read_json(list(fd.to_save()))
    print(list(fd2.to_save()))


def ceshi2():
    scr = SubCharRules()
    print([scr.and28("aaa& 12，212，32323\n&121，1212,232")])


if __name__ == '__main__':
    # ceshi()
    ceshi2()
