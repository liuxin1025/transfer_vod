#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from urllib.parse import quote
from sqlalchemy.orm import class_mapper
from settings import WX_USERINFO_GRANT_URL, WX_REDIRECT_URL, WX_CONF, WX_SYY_CONF
from lib import utils
from tornado.options import options


def model2dict(model):
    if not model:
        return {}
    fields = class_mapper(model.__class__).columns.keys()
    return dict((col, getattr(model, col)) for col in fields)

def model_to_dict(func):
    def wrap(*args, **kwargs):
        ret = func(*args, **kwargs)
        return model2dict(ret)
    return wrap

def models_to_list(func):
    def wrap(*args, **kwargs):
        ret = func(*args, **kwargs)
        return [model2dict(r) for r in ret]
    return wrap

def tuples_first_to_list(func):
    def wrap(*args, **kwargs):
        ret = func(*args, **kwargs)
        return [item[0] for item in ret]
    return wrap

def filter_update_data(func):
    def wrap(*args, **kwargs):
        if 'data' in kwargs:
            data = kwargs['data']
            data = dict([(key, value) for key, value in data.items() if value or value == 0])
            kwargs['data'] = data
        return func(*args, **kwargs)
    return wrap

def tuple_to_dict(func):
    def wrap(*args, **kwargs):
        ret = func(*args, **kwargs)
        return [dict(zip(i.keys(), i.values())) for i in ret]
    return wrap

def check_ua(func):
    def wrap(*args, **kw):
        self = args[0]
        ua = self.request.headers.get('User-Agent', '')
        if 'ThunderErp' not in ua:
            return self.render('error.tpl')
        return func(*args, **kw)
    return wrap

def wx_auth(func):
    def wrap(*args, **kw):
        self = args[0]
        openid = self.get_cookie('openid')
        if openid:
            return func(*args, **kw)
        url = WX_USERINFO_GRANT_URL.format(appid=WX_SYY_CONF['appid'], redirect_uri=quote(WX_REDIRECT_URL), state=quote(self.request.path))
        return self.redirect(url)
    return wrap

def guest_not_allow(func):
    def wrap(*args, **kw):
        self = args[0]
        if not options.debug and self.is_guest():
            raise utils.APIError(errcode=1001, errmsg='无权限操作')
        return func(*args, **kw)
    return wrap

def api_check_login(func):
    def wrap(*args, **kw):
        self = args[0]
        # wow 账号使用
        if self.get_argument('tk', '')=='6faa8040da20ef399b63a72d0e4ab575':
            self.ktv_id = int(self.get_argument('ktv_id', 0))
            self._login(dict(username='wow-test', ktv_id=self.ktv_id))
            return func(*args, **kw)

        is_login = self.get_secure_cookie('is_login')
        if not is_login:
            return self.send_json(dict(errcode=40001, errmsg='not login'))

        self.ktv_id = int(is_login.decode())
        return func(*args, **kw)
    return wrap
