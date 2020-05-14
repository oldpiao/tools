import os
import pandas as pd


class LocationTransverter(object):

    def __init__(self, dict_file, id, name, add_not_suffix_name=True):
        self.location_dict = self.read_excel(dict_file)
        if isinstance(name, (str, int)):
            name = [name]
        else:
            name = list(name)
        self.id = id
        self.name = name  # 可以为city设置多个名字，但以第一个作为输出的名字
        if add_not_suffix_name:
            self.add_not_suffix_name()
        print(self.location_dict.head())

    def add_not_suffix_name(self):
        self.location_dict[self.name[0]+"2"] = self.location_dict[self.name[0]].apply(lambda x: x[:-1])

    def read_excel(self, excel_path):
        df = pd.read_excel(excel_path, sheet_name="Sheet1", header=0)
        df = self.deal_excel(df)
        # df['行政区划代码'] = df['行政区划代码'].astype(str)
        # name_id = dict(df[["单位名称", "行政区划代码"]].values)
        # id_name = dict(df[["行政区划代码", "单位名称"]].values)
        return df

    def deal_excel(self, df):
        columns = [column for column in df.columns if isinstance(column, str)]
        print(columns)
        df = df.rename(columns=dict(map(lambda x: (x, x.strip()), df.columns)))
        for column in columns:
            df[column] = df[column].apply(lambda x: x.strip() if isinstance(x, str) else x)
        return df

    def transform(self, ns):
        locations, unknows = {}, []
        for each_city in ns[:]:
            for df_name in self.name:
                city = self.location_dict[self.location_dict[df_name] == each_city]
                if city.shape[0] == 1:
                    locations[city[self.id].values[0]] = city[self.name[0]].values[0]
                    break
                elif city.shape[0] > 1:
                    unknow = {}
                    for id, name in city[[self.id, self.name[0]]].values:
                        unknow[id] = name
                    unknows.append(unknow)
                    break
        # 处理未能准确分类的地区
        for unknow in unknows:
            # isknow = False
            for id, name in unknow.items():
                if id // 100 * 100 in locations.keys() or id // 10000 * 10000 in locations.keys():
                    locations[id] = name
                    # isknow = True
            # 目前如果无法确认准确分类则不使用该信息
            # if not isknow:  # 如果最终未能准确分类则保留最后一个作为预测的地区
            #     locations[id] = name
        # 存在子级分类的删除父级分类（标准分类唯一）
        for i in locations.copy().keys():
            if i % 100 != 0:
                k = i // 100 * 100
                if k in locations.keys():
                    locations.pop(k)
                k = i // 10000 * 10000
                if k in locations.keys():
                    locations.pop(k)
            elif i % 10000 != 0:
                k = i // 10000 * 100
                if k in locations.keys():
                    locations.pop(k)
        # if locations and unknows:
        #     print(ns, locations)
        return locations


excel_path = "行政区划字典表.xls"
lt = LocationTransverter(excel_path, "行政区划代码", ["单位名称"])