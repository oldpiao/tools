# 根据内容查找审计报告原文
import os


def get_files(file_dir, second=''):
    """轮训获取路径下的所有文件，会自动查询进一步的路径并返回拼接后的相对路径文件名"""
    for f in os.listdir(file_dir):
        if os.path.isdir(os.path.join(file_dir, f)):
            for i in get_files(os.path.join(file_dir, f), os.path.join(second, f)):
                yield i
        else:
            yield os.path.join(second, f)


def find_in_content(key, file_dir):
    for i in get_files(file_dir):
        with open(os.path.join(file_dir, i), 'r', encoding='utf-8') as f:
            data = f.read()
        if key in data:
            print('------------------------------')
            print(i)
            print('*******************')
            # print(data)
            print('\n'.join([i for i in data.split('\n') if i.strip() != '']))
            # return


def find_all_key(keys, path_and_data):
    for key in keys:
        if key not in path_and_data:
            return False
    return True


def download_in_content(keys, file_dir):
    for i in get_files(file_dir):
        with open(os.path.join(file_dir, i), 'r', encoding='utf-8') as f:
            data = f.read()
        if find_all_key(keys, path_and_data=i + "\n\n" + data):
            print(i)


if __name__ == '__main__':
    f_dir = 'D:/job/审计公告/信息抽取全项目/项目主体/数据_项目2/temp/'
    # find_in_content(key='2018年第四季度国家重大政策措施落实情况跟踪审计结果', file_dir=f_dir)
    download_in_content(keys=["人口普查", "普查"], file_dir=f_dir)
