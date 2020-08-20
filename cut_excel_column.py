# 将excel中的某列拆分成多行，并重新写入新的excel
"""
环境配置：
    # 安装处理excel的包
    pip install pandas
    pip install xlwt
获取帮助信息：
    python cut_excel_column.py -h
例子：
    python cut_excel_column.py --excel_path="test1.xlsx" --save_path="test2.xlsx" --column="a" --sep=","
"""
import argparse
import pandas as pd


def parse_args():
    def str2bool(v):
        return v.lower() in ("true", "t", "1")

    def str2int(v):
        if v.lower in ("none", "null"):
            return None
        return int(v)

    def str_or_int(v):
        try:
            v = int(v)
            return v
        except TypeError:
            return v

    parser = argparse.ArgumentParser()
    parser.add_argument("--excel_path", type=str, help="excel文件地址")  # 文件名
    parser.add_argument("--save_path", type=str, help="处理完的excel保存位置，默认为覆盖原文件，不建议覆盖原文件，会导致其他页的内容丢失")
    parser.add_argument("--column", type=str, help="待处理字段列名")  # 待处理字段列名
    parser.add_argument("--sep", type=str, default=",", help="待处理字段文本分隔符，允许使用正则，默认为：,")
    parser.add_argument("--header", type=str2int, default=0, help="设置表格头, 默认第0行为头，null或None标识无头表格")
    parser.add_argument("--sheet_name", type=str_or_int, default=0,
                        help="处理表格中的哪一页，默认第0页，取值：[0,1,2,...], [Sheet1,Sheet2,Sheet3]")
    parser.add_argument("--index_col", type=str2int, default=None, help="表个中是否包含索引，默认none,如果包含写出索引列序号")
    parser.add_argument("--save_header", type=str2bool, default=True, help="保存excel时保留文件头，默认：True")
    parser.add_argument("--save_index", type=str2bool, default=False, help="保存excel时保留文件索引，默认：Flase")
    args = parser.parse_args()
    if args.save_path is None:
        args.save_path = args.excel_path
    return args


def main(args):
    df = pd.read_excel(args.excel_path, header=args.header, sheet_name=args.sheet_name, index_col=args.index_col)
    if args.column is None:
        print(df.head())
        print("列名集合：", list(df.columns))
        args.column = input("请设置要处理的列名：")
    # df = df.apply(lambda info: cut_column(info, args), axis=1)
    df_index = df[args.column].str.split(args.sep, expand=True).stack().to_frame()
    df_index = df_index.reset_index(level=1, drop=True).rename(columns={0: args.column})
    columns1 = list(df.columns)
    columns2 = columns1.copy()
    columns2.remove(args.column)
    df = df[columns2].join(df_index)
    df = df[columns1]
    df.to_excel(args.save_path, header=True, index=False)
    print("文件已保存：%s" % args.save_path)
    # print(df.head())


if __name__ == '__main__':
    main(parse_args())
