# -*- coding: utf-8 -*-

from . import thrift_file

EncoderErrorCode = thrift_file.EncoderErrorCode
EncoderSystemException = thrift_file.EncoderSystemException
EncoderUserException = thrift_file.EncoderUserException

TRANSLATIONS = {
    EncoderErrorCode.UNKNOWN_ERROR: u'系统异常，请稍后再试',
    EncoderErrorCode.DATABASE_ERROR: u'数据库错误',
    EncoderErrorCode.TOO_BUSY_ERROR: u'系统繁忙，请稍后再试',
}


def raise_system_exc(err_code, err_msg=None):
    """
    Raise SystemException which error message shall be hide from to user.

    :param err_code: Error code defined in thrift.
    """
    raise EncoderSystemException(
        err_code,
        EncoderErrorCode._VALUES_TO_NAMES[err_code],
        err_msg or '')


def raise_user_exc(err_code, err_msg=None):
    """
    Raise UserException which error message shall be show to user.

    :param err_code: Error code defined in thrift.
    """
    translation = err_msg or TRANSLATIONS[err_code]
    raise EncoderUserException(
        err_code,
        EncoderErrorCode._VALUES_TO_NAMES[err_code],
        translation)
