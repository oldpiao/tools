import os
import tempfile

from win32com import client as wc

string_types = (str,)
text_type = str


def doc2docx(doc_file):
    '''将doc格式的文件转为docx, 建议在docx_file处设置为系统默认临时文件夹，防止处理过程导致文件生成并无法删除'''
    word = wc.Dispatch("Word.Application")
    doc = word.Documents.Open(doc_file)
    tmpfd, tempfilename = tempfile.mkstemp(suffix='.docx')
    os.close(tmpfd)
    # docx_file = os.path.splitext(doc_file)[0] + '.docx'
    # fpath, fname = os.path.split(docx_file)  # 分离文件名和路径
    # docx_file = os.path.join(tempfilename, fname)
    doc.SaveAs(tempfilename, 12)
    doc.Close()
    word.Quit()
    print('doc to docx success!')
    return tempfilename


def get_files(file_dir, second=''):
    """轮训获取路径下的所有文件，会自动查询进一步的路径并返回拼接后的相对路径文件名"""
    for f in os.listdir(file_dir):
        if os.path.isdir(os.path.join(file_dir, f)):
            for i in get_files(os.path.join(file_dir, f), os.path.join(second, f)):
                yield i
        else:
            yield os.path.join(second, f)


def strdecode(sentence):
    if not isinstance(sentence, text_type):
        try:
            sentence = sentence.decode('utf-8')
        except UnicodeDecodeError:
            sentence = sentence.decode('gbk', 'ignore')
    return sentence


def resolve_filename(f):
    try:
        return f.name
    except AttributeError:
        return repr(f)


def openfile(f):
    if isinstance(f, string_types):
        f_name = f
        f = open(f, 'rb')
    else:
        f_name = resolve_filename(f)
    return f_name, strdecode(f.read())
