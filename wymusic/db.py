# -*- coding: utf-8 -*-
'''
    @author: Clay
    @desc: 数据库
'''

from sqlalchemy import create_engine, Integer, String, Column, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///Comments.db')
Base = declarative_base()


class Comments(Base):

    __tablename__ = 'comments'

    id = Column(BigInteger().with_variant(Integer, 'sqlite'), primary_key=True, comment='ID')
    user_id = Column(Integer, nullable=True, comment='用户id')
    song_id = Column(Integer, nullable=False, comment='歌曲id')
    nickname = Column(String(32), nullable=False, comment='用户名称')
    content = Column(String(64), nullable=True, comment='评论内容')
    liked_count = Column(Integer, nullable=True, comment='点赞数')
    timed = Column(String(32), nullable=False, comment='评论时间')

    def __repr__(self):
        return '%s<%r>' % (self.__class__.__name__, self.user_id)


class Proxies(Base):

    __tablename__ = 'proxies'

    id = Column(BigInteger().with_variant(Integer, 'sqlite'), primary_key=True, comment='ID')
    address = Column(String(24), nullable=False, comment='ip地址', primary_key=True)
    protocol = Column(String(8), nullable=True, comment='协议')
    port = Column(String(4), nullable=False, comment='端口')
    used = Column(Integer, nullable=False, comment='可用')

    def __repr__(self):
        return '<%s:%s>' % (self.address, self.port)


def create_db():
    try:
        Base.metadata.create_all(engine)
        print('--------------')
        print('数据库创建完成！')
        print('--------------')
        init_db()
        print('数据库初始化完成！')
        print('---------------')
    except BaseException as e:
        print(e)


def init_db():
    pass


def drop_db():
    try:
        Base.metadata.drop_all(engine)
        print('---------------')
        print('已删除数据库文件！')
        print('---------------')
    except BaseException as e:
        print(e)


def new_session(autoflush=True, expire_on_commit=True,
                autocommit=False):
    return sessionmaker(bind=engine, autoflush=autoflush,
                        expire_on_commit=expire_on_commit,
                        autocommit=autocommit)()