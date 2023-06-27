# -*- coding:utf-8 -*-
import os
import re

from splitter.read_txt import ReadTxt
from splitter.read_excel import ReadExcel
from splitter.read_pdf.mypdfplumber import ReadPDF, ReadPDF2
from splitter.read_word import ReadDocx, ReadDoc

re_excel = re.compile(r'^\.(xlsx?|et)$', re.IGNORECASE)
re_pdf = re.compile(r'^\.(pdf)$', re.IGNORECASE)
re_doc = re.compile(r'^\.(doc|wps)$', re.IGNORECASE)
re_docx = re.compile(r'^\.(docx|wpsx)$', re.IGNORECASE)
re_txt = re.compile(r'^\.(txt)$', re.IGNORECASE)


class ReadFile(object):
    """读取任意类型文件，并带入对应模块解析，相当于一个统一的入口"""

    @classmethod
    def open_txt(cls, file_path: str, encoding='utf-8', *args, **kwargs):
        return ReadTxt.open(file_path, encoding=encoding, *args, **kwargs)

    @classmethod
    def open_excel(cls, file_path: str, header=None, *args, **kwargs):
        return ReadExcel.open(file_path, header=header, *args, **kwargs)

    @classmethod
    def open_pdf(cls, file_path: str, table_settings=None, password="", **kwargs):
        return ReadPDF.open(file_path, table_settings=table_settings, password=password, **kwargs)

    @classmethod
    def open_pdf2(cls, file_path: str, password="", **kwargs):
        """不要表格"""
        return ReadPDF2.open(file_path, password=password, **kwargs)

    @classmethod
    def open_docx(cls, file_path: str):
        return ReadDocx.open(file_path)

    @classmethod
    def open_doc(cls, file_path: str):
        return ReadDoc.open(file_path)

    @classmethod
    def open(cls, file_path: str, table_settings=None, password="", pdf_table=True, header=None, **kwargs):
        """待完善"""
        f_name, f_suffix = os.path.splitext(file_path)
        f_suffix = f_suffix.lower()
        # if '.pdf' == f_suffix:
        if re_pdf.search(f_suffix) is not None:
            if pdf_table:  # 是否处理表格
                return cls.open_pdf(file_path, table_settings=table_settings, password=password, **kwargs)
            else:
                return cls.open_pdf2(file_path, password=password, **kwargs)
        elif re_excel.search(f_suffix) is not None:
            return cls.open_excel(file_path, header=header)
        # elif '.docx' == f_suffix:
        elif re_docx.search(f_suffix) is not None:
            return cls.open_docx(file_path)
        # elif '.doc' == f_suffix or '.wps' == f_suffix:
        elif re_doc.search(f_suffix) is not None:
            return cls.open_doc(file_path)
        # elif '.txt' == f_suffix:  # 意义不大
        elif re_txt.search(f_suffix) is not None:
            return cls.open_txt(file_path)
        else:
            raise Exception('无法识别的文本格式：{0}'.format(file_path))

    def __enter__(self):
        return self


def ceshi(file_path):
    import time
    a = time.time()
    with ReadFile.open(file_path) as f:
        print(f.get_text_strs())
        # for i in f.doc:
        #     print(i.type_, i.to_save())
    print(time.time() - a)


def ceshi2(file_path):
    import time
    a = time.time()
    with ReadDoc.open(file_path) as f:
        # print(f.doc.get_text_strs())
        for i in f.doc:
            print(i.type_, i.to_save())
    print(time.time() - a)


if __name__ == '__main__':
    ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # 项目根目录
    # path = os.path.join(ROOT_DIR, "test_data/165269.pdf")  # pdf文件路径及文件名
    # path = os.path.join(ROOT_DIR, "test_data/各类型简历中信息提取可行性研究.docx")
    # path = os.path.join(ROOT_DIR, "test_data/P020181119563452108661.doc")
    # path = os.path.join(ROOT_DIR, "test_data/关于全球环境基金中国缓解大城市拥堵减少碳排放项目(成都）2018年度财务收支和项目执行情况的审计结果.wps")
    # path = os.path.join(ROOT_DIR, "test_data/审计结果公告2016年第5号（总第139号) .doc")
    # path = os.path.join(ROOT_DIR, "test_data/2016年第17号（总第168号）河南省审计厅关于郑州市轨道交通有限公司利用世界银行贷款郑州市轨道交通3号线一期工程项目2015年度项目执行情况和财务收支的审计结果公告.doc")
    # path = 'D:\\job\\审计公告\\信息抽取全项目\\项目主体\\原始数据_6.5\\datas\\云南\\审计结果公告\\2016年第5号：云南省第一人民医院新昆华医院项目建设管理情况跟踪审计结果等/审计结果公告2016年第5号（总第139号) .doc'
    # path = 'D:/job/审计公告/信息抽取全项目/项目主体/原始数据_6.5\\datas\\河南\审计公告\\2016年第17号（总第168号）河南省审计厅关于郑州市轨道交通有限公司利用世界银行贷款郑州市轨道交通3号线一期工程项目2015年度项目执行情况和财务收支的审计结果公告\\2016年第17号（总第168号）河南省审计厅关于郑州市轨道交通有限公司利用世界银行贷款郑州市轨道交通3号线一期工程项目2015年度项目执行情况和财务收支的审计结果公告.doc'
    path = 'D:/job/审计公告/信息抽取全项目/项目主体/原始数据_6.5/datas/青海/结果公告/青海省审计厅对青海省科学技术协会2013年至2015年财务收支情况的审计结果公告/青海省审计厅对青海省科学技术协会2013年至2015年财务收支情况的审计结果公告.pdf'
    # path = 'D:/job/审计公告/信息抽取全项目/项目主体/原始数据_6.5/datas/广西/审计结果公告和整改情况/广西壮族自治区审计厅2018年第15号审计结果公告：凌云县2017年扶贫政策落实和扶贫资金分配管理使用情况审计结果/广西壮族自治区审计厅2018年第15号审计结果公告：凌云县2017年扶贫政策落实和扶贫资金分配管理使用情况审计结果.pdf'
    ceshi(path)
    # ceshi2(path)
