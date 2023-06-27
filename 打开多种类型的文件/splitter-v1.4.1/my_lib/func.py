import os
import shutil
import tempfile
import logging


def get_doc(doc_file, word, remove_doc=False, retry=True):
    import pywintypes
    try:
        doc = word.Documents.Open(doc_file)
    except pywintypes.com_error as e:
        if not retry:
            if remove_doc:
                try:
                    os.remove(doc_file)
                    logging.info("中转的doc文件已被删除：%s" % doc_file)
                except PermissionError:
                    # 删除失败记录一下就算了，因为是在临时文件夹中
                    logging.warning('中转的doc文件删除失败：%s' % doc_file)
            raise e
        f_base, f_suffix = os.path.splitext(doc_file)  # 分离文件名和后缀名
        tmpfd2, temp_doc = tempfile.mkstemp(suffix=f_suffix)
        logging.info("创建中转的doc文件：%s" % temp_doc)
        os.close(tmpfd2)
        mycopyfile(doc_file, temp_doc)
        return get_doc(temp_doc, word, remove_doc=True, retry=False)
    tmpfd, temp_docx = tempfile.mkstemp(suffix='.docx')
    os.close(tmpfd)
    # doc.SaveAs(temp_docx, 12)
    doc.SaveAs(temp_docx, 12, False, "", True, "", False, False, False, False)
    doc.Close()
    if remove_doc:
        os.remove(doc_file)
        logging.info("中转的doc文件已被删除：%s" % doc_file)
    return temp_docx


def doc2docx(doc_file):
    """
    将doc格式的文件转为docx, 建议在docx_file处设置为系统默认临时文件夹，
    防止处理过程导致文件生成并无法删除, 事后应删除中间文件
    """
    try:
        from win32com import client as wc
    except ImportError as e:
        error_str = """win32com未安装，或安装存在问题:
        未安装：pip install pywin32
        安装存在问题：前往Python环境的Scripts目录下执行：python pywin32_postinstall.py -install
        详细情况参考：{}""".format("https://blog.csdn.net/ljr_123/article/details/104693372")
        logging.error(error_str)
        raise e
    word = wc.Dispatch("Word.Application")
    temp_docx = get_doc(doc_file, word)
    word.Quit()
    logging.info('doc to docx success: %s' % temp_docx)
    return temp_docx


def mycopyfile(srcfile, dstfile):
    """复制文件"""
    if not os.path.isfile(srcfile):
        logging.info("%s not exist!" % srcfile)
    else:
        fpath, fname = os.path.split(dstfile)  # 分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)  # 创建路径
        shutil.copyfile(srcfile, dstfile)  # 复制文件
        logging.info("copy %s -> %s" % (srcfile, dstfile))
