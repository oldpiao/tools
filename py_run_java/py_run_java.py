# -*- coding:utf-8 -*-
from jpype import *
import os

# 启动Java环境
startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % "*.jar", "-Djava.ext.dirs=%s" % ".")

# 加载自定义的Java Class
JClass = JClass("Base64")
jd = JClass()

authorization = jd.encode(bytes("bjm:ac76c6454085b6bb7193bbf9e8b701ea", encoding="utf-8"))
authorization = bytes(authorization).decode('utf-8')
print(authorization)
print("".join(str(hex(ord(i)))[2:] for i in authorization))
# 关闭虚拟机
shutdownJVM()
