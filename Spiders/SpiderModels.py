#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: SpiderModels.py
@time: 2017/9/17 下午1:26
"""
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DATETIME, Enum
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
import enum
import datetime

engine = create_engine('mysql+pymysql://root:root@pi/spiders', echo=True)
Base = declarative_base()


class ProxyStatus(enum.Enum):
    ok = 1,
    expired = 2,


class ProxyType(enum.Enum):
    common = 1,
    high_anonymous = 2


class HttpProxyIp(Base):
    __tablename__ = 'httpproxyip'
    id = Column(Integer, primary_key=True)
    source = Column(String(100))
    ip = Column(String(200))
    port = Column(String(100))
    proxy_type = Column(Enum(ProxyType))
    status = Column(Enum(ProxyStatus))
    created_time = Column(DATETIME, default=datetime.datetime.now())
    updated_time = Column(DATETIME, default=datetime.datetime.now())

    @staticmethod
    def __create_session__():
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        return session

    def save(self):
        session = HttpProxyIp.__create_session__()
        if not self.id:
            session.add(self)
        session.commit()
        session.close()

    @staticmethod
    def query_by_source(source):
        session = HttpProxyIp.__create_session__()
        results = session.query(HttpProxyIp).filter_by(source=source)
        session.close()
        return results

    @staticmethod
    def batch_save(models, source):
        ips = map(lambda x: x.ip, models)
        session = HttpProxyIp.__create_session__()
        results = session.query(HttpProxyIp).filter(and_(HttpProxyIp.source == source, HttpProxyIp.ip.in_(ips)))
        for m in models:
            r = list(filter(lambda x: x.ip == m.ip, results))
            if r:
                r[0].status = m.status
                r[0].updated_time = datetime.datetime.now()
                session.add(r[0])
            else:
                session.add(m)
        session.commit()


"""
if __name__ == '__main__':
    Base.metadata.create_all(engine)
    
    result = HttpProxyIp.query_by_source('test')
    for r in result:
        r.status = ProxyStatus.expired
        r.save()
    
    models = []
    p1 = HttpProxyIp(ip="1.1.1.1", status=ProxyStatus.ok, source="test")
    p2 = HttpProxyIp(ip="1.1.1.2", status=ProxyStatus.expired, source="test")
    p3 = HttpProxyIp(ip="1.1.1.3", status=ProxyStatus.expired, source="test")
    models.append(p1)
    models.append(p2)
    models.append(p3)
    HttpProxyIp.batch_save(models, source='test')
    
"""
