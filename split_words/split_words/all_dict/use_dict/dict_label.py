def label(filepath, filepath2=None, flag='xs'):
    if filepath2 is None:
        filepath2 = filepath

    mydict = ''
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for i in f.readlines():
            word = i.strip()
            if word != '':
                mydict += word + ' ' + flag + '\n'
    print(mydict)

    with open(filepath2, 'w', encoding='utf-8', errors='ignore') as f:
        f.write(mydict)


if __name__ == '__main__':
    filepath = 'D:/job/审计公告/审计问题分词/split_words/all_dict/use_dict/新违规词典732.txt'
    filepath2 = 'D:/job/审计公告/审计问题分词/split_words/all_dict/use_dict/新违规词典732_词性.txt'
    label(filepath, filepath2, flag='xs')
