from math import floor

from flask import current_app
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app import login_manager
from app.libs.enums import PendingStatus
from app.libs.helper import isbn_or_key
from app.models import Base, db
from flask_login import UserMixin

from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook


class User(UserMixin, Base):
    # __tablename__ = 'user' 这个语句会改变表名
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    # Column('password') 表示 _password 在数据库中存储名字为 'password'
    _password = Column('password', String(128), nullable=False)
    confirmed = Column(Boolean, default=False)
    # beans 鱼豆 (虚拟金币)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    @property
    def password(self):
        # 属性读取
        return self._password

    @password.setter
    def password(self, raw):
        # 属性写入
        self._password = generate_password_hash(raw)

    def can_send_drift(self):
        if self.beans < 1:
            return False
        # 在索取第三本书的时候，必须已经送出去了一本书
        success_gifts_count = Gift.query.filter_by(
            uid=self.id, launched=True
        ).count()
        success_receive_count = Drift.query.filter_by(
            requester_id=self.id, _pending=PendingStatus.Success
        ).count()

        # return True if floor(success_receive_count / 2) <= floor(success_gifts_count) else False
        if floor(success_receive_count / 2) <= floor(success_gifts_count):
            # 每索取两本书，必须赠出一本书
            return True
        else:
            return False

    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    def can_save_to_list(self, isbn):
        """
        验证数据库是否存在 isbn
        """
        if isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False
        # 不允许一个用户同事赠送多本相同的图书
        # 一个用户不能同时成为赠送者和索要者

        # 既不在赠送清单，又不在心愿清单中才能添加
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        if not gifting and not wishing:
            return True
        else:
            return False

    def generate_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode("utf-8")

    @staticmethod
    def rest_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        uid = data.get('id')
        with db.auto_commit():
            # 查询条件是主键的时候 可以直接使用 get
            # TODO user 可能为空 判断
            user = User.query.get("uid")
            user.password = new_password
        return True

    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.send_counter) + '/' + str(self.send_counter)
        )

    # def get_id(self):
    #     # login_user 要求定义的名字 继承之后就不需要了
    #     # 如果 User 类中没有定义 id, 这个函数必须重写，指定 id
    #     return self.id


@login_manager.user_loader
def get_user(uid):
    # current_user 会拥有一个 User 对象，见web/gift.py
    return User.query.get(int(uid))
