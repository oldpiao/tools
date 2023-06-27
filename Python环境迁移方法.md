综合分析平台开发

# 目录结构
- base_model_ipynb/  # (.ipynb脚本)基础模型, 与base_model_py下的模型一样，只是改为了ipynb格式
- base_model_py/  # (.py脚本)基础模型, 基于分析平台开发的模型基础脚本，使用测试数据可以直接运行，也可以拷贝出来自定义，添加自己的规则，处理自己的数据
- doc/  # (普通文件)测试数据存放位置，用于基础模型的测试与演示
	- <model_name>/  # 每个模型单独的文件夹，存放当前模型的数据
- save/ # (普通文件)测试模型时运行结果的存储位置
	- <model_name>/  # 每个模型单独的文件夹，存放当前模型的数据
- dsaa/  # (.py文件)综合分析平台核心代码，属于用于无需修改的部分
    - add_box/  # 模型的参数盒子，可以在jupyter中可视化的应用模型
	- utils/  # 用户会经常用到的一些方法, 包括数据输入输出、自定义的第三方库之类的
	- models/  # 一个个模型的核心代码，模型中用户无需修改的部分
	- settings.py  # 模块的配置文件


# 上述文件中：
	base_model/与doc/需要放在同一目录下，并配置到前端界面上
	dsaa/需要作为第三方库配置到Python环境中


# 下载依赖库，用于离线安装环境（使用该方法时应保证当前环境与目标环境系统相同，Python版本相同，否则可能存在依赖包不匹配的情况）
pip download -r requirements.txt -d ./pip_packages
或
pip download dsaa-XXX.tar.gz -d ./pip_packages

# 离线安装
pip install dsaa --no-index --find-links=./pip_packages
进入pip_packages目录执行：pip install lxml-XXX.whl

注：dsaa已经作为第三方库安装在了Python环境中，之后直接使用模型代码即可

# 更新安装
pip install --upgrade dsaa --no-index --find-links=./pip_packages

# 配置相关信息
进入目录（根据具体使用的环境可能会有所不同，目前审计署项目是在该路径下）
>>> cd /root/anaconda3/lib/python3.8/site-packages/dsaa
打开setting.py文件，配置所有双井号注释且后面有（*）的配置项
目前仅需要配置：“oss配置（*）”

# 安装注意
注：更新前建议做好，notebook模块的备份，因为notebook中有你们修改过的部分，如果修改的notebook版本与当前的其他包版本不匹配，可能会被覆盖（未验证，且一般不会不匹配，以防万一，最好备份一下）
notebook包常见位置：Anaconda3/Lib/site-packages

注2：首次部署时，最好先安装dsaa，再替换修改过的notebook包，从而尽可能避免上述问题

# 使用时可能出现的问题
如果使用时出现问题：cannot import name 'etree' from 'lxml'
原因：基础环境中包含lxml包，但版本过低
解决办法：可以使用pip_packages包重装当前的lxml
	命令：pip install --upgrade lxml --no-index --find-links=./pip_packages
	或直接进入pip_packages目录执行：pip install lxml-XXX.whl
	