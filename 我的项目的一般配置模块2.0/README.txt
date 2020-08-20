# 文档目录
# 在线安装环境
# 导出环境
# 离线安装环境
# 脚本介绍


# 系统环境: python3.7（python3以上版本都可以）

# requirements.txt  # 手写的依赖包列表，联网安装环境推荐用这个，适用性更强
# requirements2.txt  # 导出的依赖包列表，包含详细的依赖包版本信息，但也因此会造成一些不必要的错误（有些包版本并没有要求）

# 联网安装依赖包
pip install -r requirements.txt  # 安装过程出现任何问题单独安装出错的依赖包即可

# 创建虚拟环境（可选）
https://www.cnblogs.com/shyern/p/11284127.html

# 导出当前环境，（用于转移环境，使用该方法时应保证两台机器使用的Python版本相同，应使用纯净Python环境（或虚拟环境）安装相应的包后再导出）
pip freeze > requirements2.txt

# 下载依赖库，用于离线安装环境（使用该方法时应保证当前环境与目标环境系统相同，Python版本相同，否则可能存在依赖包不匹配的情况）
pip download -r requirements.txt -d ./pip_packages

# 离线安装依赖库（提前下载安装正确版本的Python，地址：https://www.python.org/downloads/）
pip install --no-index --find-links=./pip_packages -r requirements.txt

# 执行脚本位置: ./tools/
# 执行脚本说明在脚本开头，查看使用方法可以执行：python tools/脚本名.py [-h, --help]
