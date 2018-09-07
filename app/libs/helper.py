def isbn_or_key(word):
    """

    :param word:
    :return:
    """
    r = 'key'
    # ISBN 13位数字 或者 10位数字 + '-'
    if len(word) == 13 and word.isdigit():
        r = 'isbn'
    short_word = word.replace("-", '')
    if '-' in word and len(short_word) == 10 and short_word.isdiget:
        r = 'isbn'
    return r
