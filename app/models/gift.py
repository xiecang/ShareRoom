from flask import current_app
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, SmallInteger, desc, func
from sqlalchemy.orm import relationship

from app.models import Base, db
from app.spider.yushu_book import YuShuBook


class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False, unique=True)
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))
    launched = Column(Boolean, default=False)

    def is_your_self_gift(self, uid):
        return True if self.uid == uid else False

    @classmethod
    def get_user_gifts(cls, uid):
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(
            desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_list):
        from app.models.wish import Wish
        # 根据传入的isbn list  在 Wish 表计算出每个礼物的心愿数量
        # filter() 接收条件表达式 filter_by() 接受关键字参数
        # mysql in 查询
        # func.count 计算每组 Wish 的数量
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False,
            Wish.isbn.in_(isbn_list),
            Wish.status == 1).group_by(
            Wish.isbn).all()
        count_dict_list = [{'count': wish[0], 'isbn': wish[1]} for wish in count_list]
        return count_dict_list

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    # 对象代表一个礼物， 具体
    # 类代表这个事物，抽象 不是具体的'一个'
    @classmethod
    def resent(cls):
        # 链式调用
        # 主体 Query
        # 子函数 子函数返回的都是主体的类型
        # all() first() 触发函数
        # group_by + distinct 去重
        resent_gift = Gift.query.filter_by(launched=False).group_by(
            Gift.isbn
        ).order_by(
            desc(Gift.create_time)).limit(
            current_app.config["RECENT_BOOK_COUNT"]).distinct().all()
        return resent_gift
