from flask import request, flash, render_template, current_app
from flask_login import current_user

from app.libs.helper import isbn_or_key
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook
from app.view_models.book import BookCollection, BookViewModel
from app.view_models.trade import TradeInfo
from . import web
from app.forms.book import SearchForm


@web.route('/book/search')
def search():
    """
    q: 普通关键字 isbn
    page
    """
    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        # strip 去除前后空格
        q = form.q.data.strip()
        page = form.page.data
        is_bn_or_key = isbn_or_key(q)
        yushu_book = YuShuBook()

        if is_bn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)

        books.fill(yushu_book, q)
        # return jsonify(books)
        # return json.dumps(books, default=lambda o: o.__dict__)
    else:
        flash("搜索的关键词不符合要求，请重新输入关键词")
        # return jsonify(form.errors)
    return render_template("search_result.html", books=books)


@web.route("/book/<isbn>/detail")
def book_detail(isbn):
    has_in_gifts = False
    has_in_wishes = False

    # 取书籍详情数据
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)

    if current_user.is_authenticated:
        # 用户登录
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_wishes = True

    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

    trade_wishes_model = TradeInfo(trade_wishes)
    trade_gifts_model = TradeInfo(trade_gifts)

    return render_template('book_detail.html', book=book,
                           has_in_gifts=has_in_gifts,
                           has_in_wishes=has_in_wishes,
                           wishes=trade_wishes_model, gifts=trade_gifts_model)


# @web.route('/test')
# def test():
#     r = {
#         'name': None,
#         'age': 18
#     }
#     # data['age']
#     r1 = {
#
#     }
#     flash('hello,qiyue', category='error')
#     flash('hello, jiuyue', category='warning')
#     # 模板 html
#     return render_template('test.html', data=r, data1=r1)
#
#
# @web.route('/test1')
# def test1():
#     print(id(current_app))
#     from flask import request
#     from app.libs.none_local import n
#     print(n.v)
#     n.v = 2
#     print('-----------------')
#     print(getattr(request, 'v', None))
#     setattr(request, 'v', 2)
#     print('-----------------')
#     return ''
