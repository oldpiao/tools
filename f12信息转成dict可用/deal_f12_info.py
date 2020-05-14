def read(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        datalines = f.readlines()
    return datalines


def save(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(data)


def deal(readfile, savefile=None):
    datalines = read(readfile)
    new_lines = []
    for i in datalines:
        i = i.strip()
        if i == '':
            new_lines.append("")
            continue
        key = i.find(': ')
        if key != -1:
            i = i[:key] + '\": \"' + i[key+2:]
        else:
            if i[-1] == ":":
                i = i[:-1] + '\": \"'
        i = '\"' + i + '\",'
        new_lines.append(i)
    for i in new_lines:
        print(i)
    if savefile is not None:
        save(savefile, "\n".join(new_lines))


if __name__ == '__main__':
    readfile = "baidu_info.txt"
    savefile = "baidu_info_deal.txt"
    deal(readfile, savefile)
