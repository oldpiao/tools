class Base(object):
    def __init__(self):
        print("enter Base")
        self.base_key = "base_key"


class Base1(Base):
    def __init__(self, _arg1 = "_arg1 ", _arg2 = "_arg2 "):
        super(Base1, self).__init__()
        print("enter Base1" + "|" + _arg1 + "|" + _arg2)
        self.base1_key = "base1_key"


class SubBase(Base):
    def __init__(self, **kwargs):
        super(SubBase, self).__init__()
        print("enter SubBase")
        self.subbase_key = "subbase_key"


class SubBase1(Base1):
    def __init__(self, _arg1 = "_arg1 ", _arg2 = "_arg2 "):
        super(SubBase1, self).__init__(_arg1 = _arg1, _arg2=_arg2)
        print("enter SubBase1" + "|" + _arg1 + "|" + _arg2)
        self.subbase1_key = "subbase1_key"


class SubTest(SubBase, SubBase1):
    def __init__(self, _arg1="_arg1 "):
        super(SubTest, self).__init__(_arg1=_arg1, _arg2="None")
        # self.__dict__.update(vars(SubBase()))
        self.subtest_key = "subtest_key"

SubTest()
