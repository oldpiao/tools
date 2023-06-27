# pip 更换国内源（原本的源会比较慢）
# 阿里云 http://mirrors.aliyun.com/pypi/simple/
# 中国科技大学 https://pypi.mirrors.ustc.edu.cn/simple/  # 亲测好用
# 豆瓣(douban) http://pypi.douban.com/simple/
# 清华大学 https://pypi.tuna.tsinghua.edu.cn/simple/
# 中国科学技术大学 http://pypi.mirrors.ustc.edu.cn/simple/  # 亲测比较烂

pip config set global.index-url https://pypi.mirrors.ustc.edu.cn/simple/

# 安装依赖库
pip install pandas  # 表格处理
pip install python-docx  # 处理word，有一个不同版本的，不要下载错了
pip install pdfplumber  # 处理PDF，同时可以处理表格，并对其进行了一定优化
pip install pypiwin32  # 用于doc转docx

https://mirrors.tuna.tsinghua.edu.cn/pypi/web/packages/96/51/d46eb277182e0989a81cdc0933e97924b68b12519dfe62ae0ea5dec198dd/pywin32-228-cp37-cp37m-win_amd64.whl

# 生成依赖库列表
pip freeze > requirements.txt

# 一次性下载所有依赖库
pip install -r requirements.txt

linux下不需要安装win32com,但同时也将无法处理.doc文件
