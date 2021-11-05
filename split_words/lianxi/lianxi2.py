from smoothnlp import kg

rels = kg.extract(text=["SmoothNLP在V0.3版本中正式推出知识抽取功能",
                        "SmoothNLP专注于可解释的NLP技术",
                        "SmoothNLP支持Python与Java",
                        "SmoothNLP将帮助工业界与学术界更加高效的构建知识图谱",
                        "SmoothNLP是上海文磨网络科技公司的开源项目"])  ## 调用SmoothNLP解析
for rel in rels:
    print(rel)
# g = kg.rel2graph(rels)  ## 依据文本解析结果, 生成networkx有向图
# fig = kg.graph2fig(g, x=1000, y=1000)  ## 生成 matplotlib.figure.Figure 图片
# fig.savefig("SmoothNLP_KG_Demo.png") ## 保存图片到PNG


rels = kg.extract(text="SmoothNLP在V0.3版本中正式推出知识抽取功能", pretty=True)
print(rels)
"""
对输入的 text 进行 知识图谱(N元组)抽取
    :param text: 进行知识抽取的文本
        支持格式-1: str, 超过一定长度的text会被自动切句
        支持格式-2: [str], list of str
    :param pretty: 是否对词组结果进行合并, 默认True
        boolean: True/False
    :return: 知识图谱(N-元组)  -- List 
        字段: 
            subject: 对象1 
            object:  对象2
            aciton: 连接关系
            type:   连接类型
            __conf_score: 置信概率
"""
# >> [{'_conf_score': 0.9187054, 'action': '正式推出', 'object': '知识抽取功能', 'subject': 'SmoothNLP', 'type': 'action'}]