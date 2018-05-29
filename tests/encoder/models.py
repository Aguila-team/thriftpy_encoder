# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    SmallInteger,
    String,
)
from zeus_core.db import db_manager, gen_commit_deco, model_base

from zeus_core.utils import serialize_to_ttype
from . import thrift_file
from .exc import EncoderErrorCode, raise_system_exc

from zeus_core.cache import Cache, cache_mixin
from . import settings

DBSession = db_manager.get_session('encoder')
cache_manager = Cache('encoder', settings.CACHE_NAMESPACE)
region = cache_manager.make_region()
table_region = cache_manager.make_client()
cache_client = cache_manager.make_client(raw=True)

DeclarativeBase = model_base()
CacheMixin = cache_mixin(table_region, DBSession, pub=False)

auto_commit = gen_commit_deco(DBSession, raise_system_exc,
                              EncoderErrorCode.DATABASE_ERROR)


class TodoList(DeclarativeBase, CacheMixin):
    __tablename__ = 'todo_list'

    __thrift__ = thrift_file.TTodo

    id = Column(Integer, primary_key=True)
    title = Column(String, default='')
    is_done = Column(SmallInteger, default=0)
    created_at = Column(DateTime, default=datetime.datetime.now)

    @classmethod
    @region.cache_on_arguments(expiration_time=1)
    def list(cls):
        s = DBSession()
        records = s.query(cls).filter(cls.is_done == 0).all()

        return [serialize_to_ttype(r, thrift_file.TTodo) for r in records]

    @classmethod
    @auto_commit
    def add(cls, title):
        todo = cls(title=title)
        s = DBSession()
        s.add(todo)

    @classmethod
    @auto_commit
    def complete(cls, _id):
        s = DBSession()
        todo = s.query(cls).filter(cls.id == _id).first()
        if todo:
            todo.is_done = 1
            s.add(todo)
