from split_words.my_lib import func


if __name__ == '__main__':
    corpus = [
        "I come to China to travel",
        "This is a car polupar in China",
        "I love tea and Apple ",
        "The work is to write some papers in science"
    ]
    all_words = [line.split() for line in corpus]
    df = func.get_word_infos(all_words)
    print(df)
