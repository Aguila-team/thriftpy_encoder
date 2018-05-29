# -*- coding: utf-8 -*-

import logging

from . import thrift_file
from .service import service
from .models import TodoList
from .models import DeclarativeBase

from .thriftpy_encoder.decorator import decorator_builder

convert_to_thrift_structure = decorator_builder(DeclarativeBase)

logger = logging.getLogger(__name__)


@service.dispatcher
class Dispatcher(object):
    def __init__(self):
        logger.info('thriftpy.encoder server starting..')

    def ping(self):
        return True

    def scalar(self, id):
        return id

    def list_of_scalar(self, id):
        return [id] * 10

    def list_of_scalar_in_struct(self, id):
        return [id] * 10

    @convert_to_thrift_structure(thrift_file.TListOfStruct)
    def list_of_struct_in_struct(self, id_):
        class Object(object):
            pass

        return_val = []
        for i in range(10):
            o = Object()
            setattr(o, 'required_field', id_)

            return_val.append(o)

        return return_val

    @convert_to_thrift_structure(thrift_file.TEmbedData)
    def struct_of_list_in_struct(self, id_):
        class Object(object):
            pass

        return_val = []
        for i in range(10):
            o = Object()
            setattr(o, 'required_field', id_)

            return_val.append(o)

        return {
            'required_struct': o,
            'required_scalar': id_,
            'required_list_struct': return_val
        }

    @convert_to_thrift_structure(thrift_file.TMapOfStruct)
    def map_of_struct(self, id_):
        class Object(object):
            pass

        o = Object()
        setattr(o, 'required_field', id_)

        return {
            'required_map': {
                str(id_): o
            }
        }

    @convert_to_thrift_structure(thrift_file.TListOfMapOfStruct)
    def list_of_map_of_struct(self, id_):
        class Object(object):
            pass

        o = Object()
        setattr(o, 'required_field', id_)

        return [{
            'required_map': {
                id_: o
            }
        }]

    def add_todo(self, title):
        TodoList.add(title)

    def list_todo(self):
        return TodoList.list()

    def complete_todo(self, _id):
        TodoList.complete(_id)
