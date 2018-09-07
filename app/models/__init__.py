import time
from datetime import datetime

from contextlib import contextmanager
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, SmallInteger, Integer


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        """
        # contextmanager 是一个装饰器，可以给没有实现上下文管理器的类
        # 添加类似上下文管理器的方法 即在类的代码执行前后添加一些语句
        执行这个函数相当于
        try:
            gift.uid = current_user.id
            current_user.beans += current_app.confg['BEANS_UPLOAD_ONE_BOOK']
            gift.isbn = isbn
            gift.save()
        except Exception as e:
            # 异常回滚
            gift.rollback()
            raise e
        """
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)


db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    # __abstract__ 是阻止 SQLAlchemy 为 Base创建表
    __abstract__ = True
    create_time = Column('create_time', Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = int(time.time())

    def set_attrs(self, attrs_dict):
        for k, v in attrs_dict.items():
            if hasattr(self, k) and k != 'id':
                setattr(self, k, v)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def delete(self):
        self.status = 0

    def save(self):
        db.session.add(self)
        db.session.commit()

    def rollback(self):
        # 回滚
        db.session.rollback()
