import re
import os

from open_file.pdfsortdeal import PDFSortDealBase
from open_file.wordsortdeal import WordSortDealBase
from open_file.my_lib.func import openfile, doc2docx, get_files


def read_file(file_path):
    f_name, f_suffix = os.path.splitext(file_path)
    f_suffix = f_suffix.lower()
    if isinstance(file_path, str):
        if '.pdf' == f_suffix:
            return PDFSortDealBase(file_path).extract_text()
        elif '.docx' == f_suffix:
            return WordSortDealBase(file_path).extract_text()
        elif '.doc' == f_suffix:
            docx_file_path = doc2docx(file_path)
            print(docx_file_path)
            text = WordSortDealBase(docx_file_path).extract_text()
            os.unlink(docx_file_path)
            return text
        else:
            return openfile(file_path)
    else:
        return openfile(file_path)


def deal_text(text, page_rule=None, strip_space=True, rm_rules=None):
    if text is None:
        return ''
    if strip_space:
        text = text.replace(' ', '')
    if page_rule is not None:  # Common rules: r'—\s?\d+\s?—'
        if isinstance(page_rule, str):
            page_rule = [page_rule]
        for each_page_rule in page_rule:
            text = re.sub(each_page_rule, '', text)
    # Remove unnecessary parts of the string, such as header footer, page number
    if rm_rules is not None:
        if isinstance(rm_rules, str):
            rm_rules = [rm_rules]
        for rm_rule in rm_rules:
            text = re.sub(rm_rule, '', text)
    return text
