import sys
import os
import logging

import docx
from docx.document import Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph

from splitter.my_lib import func
from splitter.base.models import FileDatabase, TextData, TableData


def iter_block_items(parent):
    """
    Yield each paragraph and table child within *parent*, in document order.
    Each returned value is an instance of either Table or Paragraph. *parent*
    would most commonly be a reference to a main Document object, but
    also works for a _Cell object, which itself can contain paragraphs and tables.
    """
    if isinstance(parent, Document):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        raise ValueError("something's not right")

    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            p = Paragraph(child, parent)
            yield TextData(p.text, paragraph_style=p.style.name)
        elif isinstance(child, CT_Tbl):
            yield TableData(read_table(Table(child, parent)))


def read_table(table):
    return [[cell.text for cell in row.cells] for row in table.rows]


class ReadDocx(FileDatabase):
    """读取Word内容，目前仅读取文本内容和表格"""
    def __init__(self, parent):
        super(ReadDocx, self).__init__()
        self.parent = parent
        for i in iter_block_items(parent):
            self.add(i)

    @classmethod
    def open(cls, file_path: str, *args, **kwargs):
        doc = docx.Document(file_path)
        return cls(doc)


class ReadDoc(ReadDocx):

    @classmethod
    def open(cls, file_path: str, *args, **kwargs):
        if sys.platform != 'win32':  # win32/linux
            raise Exception("当前版本不支持Linux下处理.doc的文件，请手动转换成.docx格式后使用，或在windows系统下使用: %s" % file_path)
        docx_file_path = func.doc2docx(file_path)
        doc = docx.Document(docx_file_path)
        os.remove(docx_file_path)
        logging.info("中间文件已被删除：%s" % docx_file_path)
        return cls(doc)
