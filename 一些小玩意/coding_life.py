# 注：所有未写明方法皆有返回，会直接print函数名，请最后将print结果发给我
import time
import datetime
import random


class Human(object):
    pass


class 琳鹅Human(Human):
    def 做娃娃菜火腿肠粉丝(self):
        res = "ヾ(✿ﾟ▽ﾟ)ノ"
        print("琳鹅做娃娃菜火腿肠粉丝")
        print(res)
        return res

    def 做黄瓜肉片鸡蛋(self):
        res = "\(^o^)/~"
        print("琳鹅做黄瓜肉片鸡蛋")
        print(res)
        return res


class 朴朴Human(Human):
    def __init__(self, cooking_state=True, is_foolish=False, force_state=None):
        self.cooking_state = "想做饭" if cooking_state else "不想做饭"
        self.is_foolish = is_foolish
        self.cookbook = ["打开B站朴朴菜谱300", "做藕", "任意发挥"]
        self.cookbook_map = {
            "做藕": self.做藕,
        }
        self.state_map = ["想建博"] + ["想回东亚上北待一天"] + ["想我对象"] * 10000
        self.force_state = force_state

    def get_state(self):
        if self.force_state is None:
            res = random.choice(self.state_map)
        else:
            res = self.force_state
        print(res)
        if res == "想建博":
            print("额，yue~~~")
            if self.force_state == res:
                self.force_state = None
            return self.get_state()
        return res

    def get_cooking_state(self):
        return self.cooking_state

    def 提出想吃什么(self):
        res = random.choice(self.cookbook)
        print(res)
        return res

    def get_forward_state(self):
        if self.is_foolish:
            res = "想不出吃什么"
            print(res)
            return res
        return self.提出想吃什么()

    def 给琳鹅打电话(self):
        res = "(＾－＾)V"
        return res

    def 做藕(self):
        res = "藕+肉丝+水+油+调料=爆炒藕丁"
        return res

    def 任意发挥(self):
        while True:
            key = random.choice(self.cookbook)
            if key in self.cookbook_map.keys():
                res = self.cookbook_map[key]()
                print(res)
                return res
            else:
                print("暂未收录【{}】做法，换一道菜吧".format(key))


def 去东亚上北(朴朴: 朴朴Human, cur_time="23:20"):
    print("去东亚上北")
    cur_time_str = "2022-07-14 " + cur_time
    date_int = datetime.datetime.strptime("2022-07-14", "%Y-%m-%d").timestamp()
    cur_time_int = datetime.datetime.strptime(cur_time_str, "%Y-%m-%d %H:%M").timestamp() - date_int

    # if cur_time == "23：20":
    while True:
        now_date_str = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        now_date_int = datetime.datetime.strptime(now_date_str, "%Y-%m-%d").timestamp()
        now_time = time.time() - now_date_int
        if now_time >= cur_time_int:
            return 朴朴.给琳鹅打电话()
        print("再过{}秒给琳鹅打电话。。。".format(int(cur_time_int-now_time)))
        time.sleep(10)


def 去友谊嘉园(朴朴:朴朴Human, 琳鹅:琳鹅Human):
    print("去友谊嘉园")
    if 朴朴.get_cooking_state() == "不想做饭":
        if 朴朴.get_forward_state() == "想不出吃什么":
            琳鹅.做娃娃菜火腿肠粉丝()
            琳鹅.做黄瓜肉片鸡蛋()
        else:
            朴朴.提出想吃什么()
    else:
        朴朴.做藕()
        朴朴.任意发挥()


def 执行晚上流程(朴朴:朴朴Human):
    琳鹅 = 琳鹅Human()
    state = 朴朴.get_state()
    if not state == "想建博" and not state == "想回东亚上北待一天":
        去友谊嘉园(朴朴, 琳鹅)
    else:
        去东亚上北(朴朴)


if __name__ == '__main__':
    执行晚上流程(朴朴Human())
    # print("-------功能测试----------------------")
    # 执行晚上流程(朴朴Human(cooking_state=False, is_foolish=False))
    # print("-------功能测试----------------------")
    # 执行晚上流程(朴朴Human(cooking_state=False, is_foolish=True))
    # print("-------功能测试----------------------")
    # 执行晚上流程(朴朴Human(cooking_state=False, is_foolish=True, force_state="想建博"))
    # print("-------功能测试----------------------")
    # 执行晚上流程(朴朴Human(cooking_state=False, is_foolish=True, force_state="想回东亚上北待一天"))
