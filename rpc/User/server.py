# -*- coding: utf-8 -*-
# @File    : server.py
# @AUTH    : model_creater

import os
import json
from bson import ObjectId
from datetime import datetime
import thriftpy2
from thriftpy2.rpc import make_server
from tornado.util import ObjectDict
from rpc.utils import render_thrift
from apps.user import utils
from apps.errors import AppResourceError as ResourceError
from rpc import base


rpc_dir = os.path.abspath(os.path.dirname(__file__))

user_thrift = thriftpy2.load(rpc_dir + "/protocols/user.thrift",
                             module_name="user_thrift")


class UserDispatcher(BaseDispatcher):
    pass