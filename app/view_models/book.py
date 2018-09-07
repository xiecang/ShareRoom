class BookViewModel:
    def __init__(self, book):
        self.title = book.get("title")
        self.publisher = book.get("publisher")
        self.pages = book.get("pages")
        # self.author = book.get("author")
        self.author = "、".join(book["author"])
        self.price = book.get("price")
        self.summary = book.get("summary")
        self.image = book.get("image")
        self.isbn = book.get('isbn')
        self.pubdate = book.get('pubdate')
        self.binding = book.get('binding')

    @property
    def intro(self):
        # 装饰器 property 是用属性的方式调用函数
        intros = filter(lambda x: True if x else False,
                        [self.author, self.publisher, self.price])
        return '/'.join(intros)


class BookCollection:
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, yushu_book, keyword):
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in yushu_book.books]


class _BookViewModel:
    @classmethod
    def package_single(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword,
        }
        if data:
            returned['total'] = 1
            returned['books'] = [cls.__cut_book_data(data)]
        return returned

    @classmethod
    def package_collection(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword,
        }
        if data:
            returned['total'] = data.get("total")
            returned['books'] = [cls.__cut_book_data(book) for book in data.get("books")]
        return returned

    @classmethod
    def __cut_book_data(cls, data):
        book = {
            'title': data['title'],
            "publisher": data["publisher"],
            "pages": data["pages"] or '',
            # "author": "、".join(data["author"]),
            "author": data["author"],
            "price": data["price"],
            "summary": data["summary"] or '',
            "image": data["image"],
        }
        return book
