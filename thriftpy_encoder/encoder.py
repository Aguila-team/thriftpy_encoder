from functools import partial, wraps
import json
import time
import datetime
from enum import Enum


def convert_rich_feature_object_to_plaint_object(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        if isinstance(result, datetime.datetime) and result.tzinfo is None:
            return int(time.mktime(result.timetuple()))
        if isinstance(result, datetime.date):
            return result.isoformat()

        return result

    return wrapper


class ThriftEncoder(object):
    @classmethod
    def _process_scalar(cls, thrift_type, value):
        if thrift_type == 8 and isinstance(value, Enum):
            # i32 type
            return value.value
        if thrift_type == 11:
            # string type
            if isinstance(value, dict):
                return json.dumps(value)
            return unicode(value)

        # other type no need more encode: str, int ...
        return value

    @classmethod
    def _convert(cls, target_type, result):
        # dispatch to other real processor
        if isinstance(target_type, tuple):
            return cls._process_complex_structure(target_type, result)

        if isinstance(target_type, int):
            if target_type in (2, 3, 9, 10, 4, 11, 16, 17):
                return cls._process_scalar(target_type, result)

        return cls._process_simple_structure(target_type, result)

    @classmethod
    @convert_rich_feature_object_to_plaint_object
    def get_attr_or_key_value_of_obj(cls, obj, k):
        # type: (object, string) -> object

        print("{} -> {}".format(obj, k))

        # NOTE: disabled for better solution
        # if isinstance(obj, self.sqlalchemy_declarative_base):
        #     obj = self._turn_sqlalchemy_object_to_dict(obj)

        if isinstance(obj, dict) and k in obj:
            return obj[k]

        v = getattr(obj, k, None)
        if v is not None:
            return v

        return None

    @classmethod
    def _process_simple_structure(cls, target_type, result):
        thrift_result = dict(target_type.default_spec)

        for spec in target_type.thrift_spec.values():
            thrift_type = None
            element_type = None
            is_required = False

            if len(spec) == 3:
                thrift_type, name, is_required = spec
            if len(spec) == 4:
                thrift_type, name, element_type, is_required = spec

            sub_result_item = cls.get_attr_or_key_value_of_obj(result, name)

            if sub_result_item is None and is_required:
                raise ValueError("Field {} is required, but not provide!".format(name))

            if sub_result_item is not None:
                if thrift_type == 12:  # struct
                    thrift_result[name] = cls._process_simple_structure(element_type, sub_result_item)
                elif thrift_type == 15:  # list
                    thrift_result[name] = cls._process_complex_structure((thrift_type, element_type), sub_result_item)
                elif thrift_type == 13:  # map
                    keyword_thrift_type, (value_thrift_type, value_element_type) = element_type
                    thrift_result[name] = {}
                    for k, v in sub_result_item.items():
                        structed_v = cls._process_complex_structure((value_thrift_type, value_element_type), v)

                        thrift_result[name][k] = structed_v
                else:
                    # other type
                    thrift_result[name] = cls._process_scalar(thrift_type, sub_result_item)

        return target_type(**thrift_result)

    @classmethod
    def _process_complex_structure(cls, target_type, result):
        if isinstance(target_type, tuple):  # is complex structure
            container_type, inner_element_type = target_type
            if container_type == 15:  # list
                if isinstance(inner_element_type, tuple):   # complex sub-element
                    return map(partial(cls._process_complex_structure, inner_element_type), result)
                if isinstance(inner_element_type, int):  # scalar element
                    return map(partial(cls._process_scalar, inner_element_type), result)

            if container_type == 12:  # struct
                return cls._process_simple_structure(inner_element_type, result)

    @classmethod
    def encode(cls, target, result):
        return cls._convert(target, result)
