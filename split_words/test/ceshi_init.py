import split_words

mr = split_words.RePOSTokenizer()
mr.add_word(word=r'abc', freq=None, tag='aa@bb')
mr.add_word(word=r'aaa', freq=None, tag='aa@cc')
sentence = r'aaabcnnaaajnabckjsdkaaasjdabcaksjka'
print([type(word) for word in mr.pws_cut(sentence).words])
