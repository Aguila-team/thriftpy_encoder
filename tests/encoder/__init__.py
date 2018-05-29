# -*- coding: utf-8 -*-

import thriftpy
from os import path

current_path = path.dirname(path.abspath(__file__))
thrift_file = thriftpy.load('encoder/encoder.thrift',
                            'encoder_thrift')
