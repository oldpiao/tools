class FenCi(object):
    def __init__(self, begins, ends, words):
        self.begins = begins
        self.ends = ends
        self.words = words

    def begin_find_end(self, begin):
        return self.ends[self.begins.index(begin)]

    def deal_spetialsigns(self):
        new_words, new_word, end = [], '', None
        # for word in self.words:
        i = 0
        while i < len(self.words):
            if self.words[i] in self.begins:
                end = self.begin_find_end(self.words[i])
                try:
                    find_end = self.words[i+1:].index(end) + i + 1
                    new_words.append(''.join(self.words[i:find_end + 1]))
                    i = find_end
                except:
                    new_words.append(self.words[i])
            else:
                new_words.append(self.words[i])
            i += 1
        self.words = new_words


def zhuanyi(rule):
    key_sites, begin = [], 0
    while True:
        key_site = rule[begin:].find('\\')
        # print(key_site, begin, rule[begin:])
        if key_site == -1:
            break
        else:
            begin += key_site
            if begin+1 >= len(rule):
                break
            key_sites.append([begin, rule[begin+1]])
            rule = rule[:begin] + rule[begin+2:]
    print(key_sites)


if __name__ == '__main__':
    print(zhuanyi('ab\/c\de/fgh\/igklm\/\nop\qrstu/vwxyz\\'))
    print(zhuanyi('\d+'))
