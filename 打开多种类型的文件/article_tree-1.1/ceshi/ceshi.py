a = {'status': {'status': True, 'status_info': None}, 'data': {'lines': [['（一）bbb'], ['cccc'], ['ddddd']], 'line_types': [1, -1, -1], 'line_nums': ['一', None, None]}}


def deal_1(d, r):
    for n, i in enumerate(d):
        if i == 1:
            r["1"] = d[n:]
    return r


def deal_all_2(d, r):
    b = []
    for n, i in enumerate(d):
        if i == 2:
            b.append(i)
    r["2"] = b
    return r


def deal_all__1(d, r):
    b = []
    for n, i in enumerate(d):
        if i == -1:
            b.append(i)
    r["-1"] = b
    return r


data = [1, -1, -1, 2, 2]


res = {}
# for deal in [deal_1, deal_all_2, deal_all__1]:
#     r = deal(data, res)
r = deal_1(data, res)
r = deal_all_2(data, res)
r = deal_all__1(data, res)

print(res)


class Sentence(object):
    def __init__(self, string):
        self.string = string
        self.title = True
        self.title_name = 1

    def is_title(self):
        return


class Content(object):
    def __init__(self, sentences: list):
        self.sentences = sentences

    def find_all_title(self):
        for sentence in self.sentences:
            if sentence.is_title():
                yield sentence
