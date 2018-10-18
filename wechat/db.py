# -*- coding: utf-8 -*-
'''
@Author: Clay
@Module Function: 数据库表格对应类
@Last Modified By: Clay
@Last Modified Time: 2018-10-15
@Last Modified Content:
'''
from sqlalchemy import create_engine, String, Column, BigInteger, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///Proxies.db', echo=True)
Base = declarative_base()


class Proxy(Base):
    '''代理类'''
    __tablename__ = 'proxy'

    id = Column(BigInteger().with_variant(Integer, 'sqlite'), primary_key=True, comment='ID')
    address = Column(String(16), nullable=True, comment='地址')
    protocol = Column(String(8), nullable=True, comment='协议')
    port = Column(String(8), nullable=True, comment='端口')

    def __repr__(self):
        return '<Proxy %r>' % self.address


class Article(Base):
    '''文章类'''
    __tablename__ = 'article'

    id = Column(BigInteger().with_variant(Integer, 'sqlite'), primary_key=True, comment='ID')
    public_name = Column(String(16), nullable=False, comment='公众号名称')
    article_name = Column(String(24), nullable=False, comment='文章名称')
    content = Column(String(512), nullable=False, comment='文章内容')

    def __repr__(self):
        return '<Name %r>' % self.public_name


class Public(Base):
    '''公众号类'''
    __tablename__ = 'public'

    id = Column(BigInteger().with_variant(Integer, 'sqlite'), primary_key=True, comment='ID')
    public_name = Column(String(16), nullable=False, comment='公众号名称')
    function = Column(String(64), nullable=True, comment='功能介绍')
    certification = Column(String(32), nullable=True, comment='微信认证')
    recent_article = Column(String(64), nullable=True, comment='最近文章')

    def __repr__(self):
        return '<Public name %r>' % self.public_name


def create_db():
    try:
        Base.metadata.create_all(engine)
        print('数据库创建完成.')
        init_db()
        print('数据初始化完成.')
    except BaseException as e:
        print(e)


def init_db():
    pass


def drop_db():
    try:
        Base.metadata.drop_all(engine)
        print('数据库已移除.')
    except BaseException as e:
        print(e)


def new_session(autoflush=True, exprire_on_commit=True,
                autocommit=False):
    return sessionmaker(bind=engine, autoflush=autoflush,
                        expire_on_commit=exprire_on_commit,
                        autocommit=autocommit)()