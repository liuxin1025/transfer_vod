import os
import re
import json
import when
import math
import logging
from datetime import datetime, timedelta
import hashlib
import random
import base64

from control import ctrl
from handler.base import BaseHandler
from tornado.httputil import url_concat
from settings import ORDER_CHANNEL, ORDER_TP, BILL_TP, FAST_RATE
from tornado import web, gen
from lib import utils
import calendar
from tornado.options import options
from lib.decorator import guest_not_allow, api_check_login


class BindHandler(BaseHandler):

    async def get(self):
        self.send_json({'url': 'bind'})



class UnbindHandler(BaseHandler):

    async def get(self):
        self.send_json({'url': 'unbind'})

