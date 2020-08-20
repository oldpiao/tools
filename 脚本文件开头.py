import os
import sys
import argparse  # 参数设置

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.append(os.path.abspath(os.path.join(__dir__, '..')))
# 上面三行代码是为了将当前路径和上一层路径添加到path中
# 否则会导致，脚本不在项目根目录时，无法访问项目相关包的问题
# 本地库一定在这三行代码后再调用


def parse_args():
    """参数设置"""
    def str2bool(v):
        """自定义参数类型"""
        return v.lower() in ("true", "t", "1")

    parser = argparse.ArgumentParser()
    parser.add_argument("--excel_path", type=str, help="excel文件地址")  # 文件名
    parser.add_argument("--save_path", type=str, help="处理完的excel保存位置，默认为覆盖原文件，不建议覆盖原文件，会导致其他页的内容丢失")
    parser.add_argument("--save_header", type=str2bool, default=True, help="保存excel时保留文件头，默认：True")
    args = parser.parse_args()
    if args.save_path is None:
        args.save_path = args.excel_path
    return args
	
	
def main(args):
    print(args)


if __name__ == '__main__':
    main(parse_args())

