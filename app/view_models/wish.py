# from collections import namedtuple

from app.view_models.book import BookViewModel

# namedtuple 可以快速创建一个对象
# MyGift = namedtuple('MyGift', ['id', 'book', 'wishes_count'])


class MyWishes:
    def __init__(self, gift_of_mine, wish_count_list):
        self.wishes = []

        self.__gift_of_mine = gift_of_mine
        self.__wish_count_list = wish_count_list

        self.wishes = self.__parse()

    def __parse(self):
        tmp_gift = []
        for gift in self.__gift_of_mine:
            my_gift = self.__matching(gift)
            tmp_gift.append(my_gift)
        return tmp_gift

    def __matching(self, gift):
        count = 0
        for wish_count in self.__wish_count_list:
            if gift.isbn == wish_count['isbn']:
                count = wish_count['count']
        # my_gift = MyGift(gift.id, BookViewModel(gift.book), count)
        # return my_gift
        r = {
            'wishes_count': count,
            'book': BookViewModel(gift.book),
            'id': gift.id,
        }
        return r
