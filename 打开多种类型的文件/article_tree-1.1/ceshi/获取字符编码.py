def get_utf8(str):
    res = [chr(ord(str) + i) for i in range(30)]
    print(res)
    return res


if __name__ == '__main__':
    get_utf8("㊀")
    get_utf8("㈠")
    get_utf8("①")

