from app.libs.httper import HTTP
from flask import current_app


class YuShuBook:
    """
    http://t.yushu.im/v2/book/isbn/{}
    http://t.yushu.im/v2/book/search?q={}&count={}&start={}
    """
    isbn_url = "http://t.yushu.im/v2/book/isbn/{}"
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn)
        result = HTTP.get(url)
        self.__fill_single(result)

    def search_by_keyword(self, keyword, page=1):
        url = self.keyword_url.format(keyword, current_app.config["PER_PAGE"], self.calculate_start(page))
        result = HTTP.get(url)
        self.__fill_collection(result)

    @staticmethod
    def calculate_start(page):
        return (page - 1) * current_app.config["PER_PAGE"]

    def __fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self, data):
        self.total = data['total']
        self.books = data['books']

    @property
    def first(self):
        # 验证是否存在本书
        return self.books[0] if self.total >= 1 else None
