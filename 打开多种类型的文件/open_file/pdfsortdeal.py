import re
import os, time
from collections import Iterable

# import pdf2txt  # 直接使用该方法内的方法，并对其进行了修改
import sys
import pdfminer.settings
pdfminer.settings.STRICT = False
import pdfminer.high_level
import pdfminer.layout
from pdfminer.image import ImageWriter

from open_file.settings import logger


class PDFSortDealBase(object):

    def __init__(self, fname, password="", *args, **kwargs):
        self.fname = fname
        self.set_text_pages(fname=fname, password=password, *args, **kwargs)

    def set_text_pages(self, fname, password="", *args, **kwargs):
        # 该步骤会生成缓存文件，有可能会在程序异常时无法成功删除缓存文件
        outfile = str(time.time()) + '.txt'
        try:
            with open(outfile, 'wb') as outfp:
                outfp = pdf2txt_extract_text(files=[fname], outfp=outfp,
                                             password=password, *args, **kwargs)
            with open(outfile, 'r', errors='ignore', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            logger.debug('PDF文件解析失败: %s 中间文件: %s' % (fname, outfile))
            raise e
        finally:
            os.remove(outfile)
            logger.info('中间文件已删除: %s' % outfile)
        text = text.replace('\xa0', '\n')  # 特殊字符处理，\xa0 是不间断空白符 &nbsp;
        self.all_text = text.replace('\x0c', '\n')
        self.pages = text.split('\x0c')
        if text[-1] is '\x0c':
            self.pages = self.pages[:-1]
        return self

    def extract_text(self, page_numbers=None):
        '''
        :param page_numbers: default None, all text
        '''
        if page_numbers is None:
            text = self.all_text[:]
        elif isinstance(page_numbers, int):
            text = self.pages[page_numbers][:]
        elif isinstance(page_numbers, Iterable):
            try:
                text = ''.join(self.pages[i] for i in page_numbers)
            except Exception:
                logger.debug('page_numbers must be an array of Numbers or Numbers or None.')
                raise Exception('page_numbers must be an array of Numbers or Numbers or None.')
        else:
            logger.debug('page_numbers must be an array of Numbers or Numbers or None.')
            raise Exception('page_numbers must be an array of Numbers or Numbers or None.')
        return text


def pdf2txt_extract_text(files=[], outfile='-', outfp=None,
                         _py2_no_more_posargs=None,  # Bloody Python2 needs a shim
                         no_laparams=False, all_texts=None, detect_vertical=None, # LAParams
                         word_margin=None, char_margin=None, line_margin=None, boxes_flow=None, # LAParams
                         output_type='text', codec='utf-8', strip_control=False,
                         maxpages=0, page_numbers=None, password="", scale=1.0, rotation=0,
                         layoutmode='normal', output_dir=None, debug=False,
                         disable_caching=False, **other):
    if _py2_no_more_posargs is not None:
        raise ValueError("Too many positional arguments passed.")
    if not files:
        raise ValueError("Must provide files to work upon!")

    # If any LAParams group arguments were passed, create an LAParams object and
    # populate with given args. Otherwise, set it to None.
    if not no_laparams:
        laparams = pdfminer.layout.LAParams()
        for param in ("all_texts", "detect_vertical", "word_margin", "char_margin", "line_margin", "boxes_flow"):
            paramv = locals().get(param, None)
            if paramv is not None:
                setattr(laparams, param, paramv)
    else:
        laparams = None

    imagewriter = None
    if output_dir:
        imagewriter = ImageWriter(output_dir)

    if output_type == "text" and outfile != "-":
        for override, alttype in (  (".htm", "html"),
                                    (".html", "html"),
                                    (".xml", "xml"),
                                    (".tag", "tag") ):
            if outfile.endswith(override):
                output_type = alttype

    if outfp is not None:
        pass
    elif outfile == "-":
        outfp = sys.stdout
        if outfp.encoding is not None:
            codec = 'utf-8'
    else:
        outfp = open(outfile, "wb")
    for fname in files:
        with open(fname, "rb") as fp:
            pdfminer.high_level.extract_text_to_fp(fp, **locals())
    return outfp