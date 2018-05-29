import functools

from .encoder import ThriftEncoder


def convert_to_thrift_structure(thrift_structure):
    def deco_func(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            encoded_result = ThriftEncoder.encode(thrift_structure, result)

            return encoded_result

        return wrapper

    return deco_func
