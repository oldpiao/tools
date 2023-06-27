from splitter.base.models import FileDatabase, TextData


__all__ = ['ReadTxt']


class ReadTxt(FileDatabase):
    """读取Word内容，目前仅读取文本内容和表格"""
    def __init__(self, lines):
        super(ReadTxt, self).__init__()
        for line in lines:
            self.add(TextData(line))

    @classmethod
    def open(cls, file_path: str, encoding='utf-8', *args, **kwargs):
        with open(file_path, 'r', encoding=encoding) as f:
            doc = f.read().split('\n')
        return cls(doc)
