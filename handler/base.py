#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import traceback
import re
import json

from tornado import web
from control import ctrl
from lib import uimethods, utils
from settings import ERR_MSG
from raven.contrib.tornado import SentryMixin
from tornado.options import options


_COOKIE_KEY =lambda ktv_id, appid: 'GZH_openid_2_%s_%s'%(str(ktv_id), appid)
WX_CONF = {
    'appid': 'wxd7db9db45b020ac8',
    'appsecret': 'e520b41e21f508fc7e70a5698b3ca75a',
}

if options.debug:
    WX_CONF = {
        'appid': 'wxb74f4a965c0baaae',
        'appsecret': 'c16d564d0f679b8072bcee83f5fa280f',
    }


class BaseHandler(web.RequestHandler, SentryMixin):

    MOBILE_PATTERN = re.compile('(Mobile|iPod|iPhone|Android|Opera Mini|BlackBerry|webOS|UCWEB|Blazer|PSP)', re.I)

    def _d(self):
        if self.MOBILE_PATTERN.search(self.request.headers.get('user-agent', '')):
            return 'mobile'
        else:
            return 'pc'

    def is_guest(self):
        is_guest = self.get_secure_cookie('is_guest')
        ret = int(is_guest) if is_guest else 0
        return ret

    def dict_args(self):
        _rq_args = self.request.arguments
        rq_args = dict([(k, _rq_args[k][0].decode()) for k in _rq_args])
        logging.info(rq_args)
        return rq_args

    def initialize(self):
        ctrl.pdb.close()
        #if options.debug:
        #    self.set_cookie('gzh_openid', 'o7OwQwe14Hs9xqWZxTDALiV4QlqQ')

    def on_finish(self):
        ctrl.pdb.close()

    def send_json(self, data={}, errcode=200, errmsg='', status_code=200):
        res = {
            'errcode': errcode,
            'errmsg': errmsg if errmsg else ERR_MSG[errcode]
        }
        res.update(data)
        self.set_header('Content-Type', 'application/json')
        full_paths = ['/gzh_custom/gzh/api/buffet', '/gzh_custom/gzh/lottery/activity']
        paths = ['/gzh_custom/gzh/branch/count']

        if self.request.path in full_paths:
            self.set_header("Access-Control-Allow-Origin", "*")
            self.set_header("Access-Control-Allow-Headers", "x-requested-with")
            self.set_header('Access-Control-Allow-Methods', 'GET')
        for path in paths:
            if self.request.path in path:
                self.set_header("Access-Control-Allow-Origin", "*")
                self.set_header("Access-Control-Allow-Headers", "x-requested-with")
                self.set_header('Access-Control-Allow-Methods', 'GET')
                break

        self.set_status(status_code)
        json_str = uimethods.json_format(self, res)
        if options.debug:
            logging.info('path: %s, method: %s, arguments: %s, response: %s' % (self.request.path, self.request.method,
                                                                                self.request.arguments, json_str))
        self.write(json_str)

    def write_error(self, status_code=200, **kwargs):
        if 'exc_info' in kwargs:
            err_object = kwargs['exc_info'][1]
            traceback.format_exception(*kwargs['exc_info'])

            if isinstance(err_object, utils.APIError):
                err_info = err_object.kwargs
                self.send_json(**err_info)
                return

        self.send_json(status_code=500, errcode=50001)
        if not options.debug:
            return self.captureException(**kwargs)

    def get_secure_cookie(self, name, **kwargs):
        cookie = super(BaseHandler, self).get_secure_cookie(name, **kwargs)
        logging.info(cookie)
        return cookie

    def get_current_user(self):
        username = self.get_secure_cookie('erp_ktvsky_com')
        if not username:
            self._logout()
            return
        return username.decode()

    def _login(self, user):
        username = str(user['username'])
        self.set_secure_cookie('erp_ktvsky_com', username, expires_days=1)
        self.set_secure_cookie('is_login', str(user['ktv_id']), expires_days=1)
        self.set_secure_cookie('is_guest', '0')

    def _logout(self):
        self.clear_cookie('erp_ktvsky_com')
        self.current_user = None

    def render(self, template_name, **kwargs):
        tp = self.get_argument('tp', '')
        if tp=='out':
            kwargs.update({'show_menu': 1, 'tp': 'out'})
        else:
            kwargs.update({'show_menu': 0, 'tp': tp})

        if options.debug:
            logging.info('render args: %s' % kwargs)
        return super(BaseHandler, self).render(template_name, **kwargs)

    def is_actived_ktv(self, ktv_id):
        #if options.debug:
        #    return True

        if ctrl.rs.sismember(ctrl.custom.get_custem_active_key_ctl(), int(ktv_id)):
            return 1

        return 0

    def is_ktv_module_setted(self, ktv_id, tp='coupon'):
        #if options.debug:
        #    return 1

        if ctrl.custom.check_ktv_set_module_ctl(ktv_id, tp):
            return 1

        return 0

    def is_ktv_setted(self, ktv_id):
        if options.debug:
            return 1
        if ctrl.custom.check_ktv_setted_ctl(ktv_id):
            return 1
        return 0

    def need_active(self):
        self.render('error.html', err_title='功能未激活', err_info='该功能未激活，请联系您的代理商激活')

    def need_setting(self):
        self.render('error.html', err_title='功能未设置', err_info='该功能设置有误，请联系您的代理商设置')

    def render_empty(self, err_title='收银员等级', err_info='该活动已过期'):
        self.render('error.html', err_title=err_title, err_info=err_info)

    def get_openid_cookie_of_ktv(self, ktv_id):
        ktv_wx = ctrl.custom.get_ktv_wx_ctl(int(ktv_id))
        appid = ktv_wx.get('appid', WX_CONF['appid'])
        openid = self.get_cookie(_COOKIE_KEY(ktv_id, appid))
        return openid

