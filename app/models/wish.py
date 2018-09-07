from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, SmallInteger, desc, func
from sqlalchemy.orm import relationship

from app.models import Base, db
from app.spider.yushu_book import YuShuBook


class Wish(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False, unique=True)
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))
    launched = Column(Boolean, default=False)

    @classmethod
    def get_user_wishes(cls, uid):
        wishes = Wish.query.filter_by(uid=uid, launched=False).order_by(
            desc(Wish.create_time)).all()
        return wishes

    @classmethod
    def get_gift_counts(cls, isbn_list):
        from app.models.gift import Gift
        # 根据传入的isbn list  在 Wish 表计算出每个礼物的心愿数量
        # filter() 接收条件表达式 filter_by() 接受关键字参数
        # mysql in 查询
        # func.count 计算每组 Wish 的数量
        count_list = db.session.query(func.count(Gift.id), Gift.isbn).filter(
            Gift.launched == False,
            Gift.isbn.in_(isbn_list),
            Gift.status == 1).group_by(
            Gift.isbn).all()
        count_dict_list = [{'count': gift[0], 'isbn': gift[1]} for gift in count_list]
        return count_dict_list

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first
