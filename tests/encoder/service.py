# -*- coding: utf-8 -*-

from zeus_core.service import Service
from . import thrift_file

service = Service(
    timeout=3 * 1000,

    thrift=thrift_file,
    service_name='EncoderService',

    user_exc=thrift_file.EncoderUserException,
    system_exc=thrift_file.EncoderSystemException,
    unknown_exc=thrift_file.EncoderUnknownException,
    error_code=thrift_file.EncoderErrorCode,
)

from dispatcher import *  # noqa Register dispatcher in this.