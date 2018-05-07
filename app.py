#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import uuid
import base64

from tornado import web
from tornado.options import options
from lib import uimodules, uimethods
from tornado.httpserver import HTTPServer
from raven.contrib.tornado import AsyncSentryClient
from tornado.web import StaticFileHandler


STATIC_PATH = os.path.join(sys.path[0], 'static')
URLS = [
    (r'(\d+)\.ngrok\.ktvsky\.com',

        (r'/room/bind', 'handler.room.BindHandler'),
        (r'/room/unbind', 'handler.room.UnbindHandler'),
        # (r'/room/ulist', 'handler.room.UlistHandler'),
        # (r'/room/getroominfo', 'handler.room.InfoHandler'),
        # (r'/song/vod', 'handler.song.VodHandler'),
        # (r'/song/list', 'handler.song.ListHandler'),
        # (r'/song/completelist', 'handler.song.CompleteListHandler'),
        # (r'/song/next', 'handler.song.NextHandler'),
        # (r'/song/ptoggle', 'handler.song.PtoggleHandler'),
        # (r'/song/ctoggle', 'handler.song.CtoggleHandler'),
        # (r'/song/mvol', 'handler.song.VolHandler'),
        # (r'/song/mmic', 'handler.song.MicHandler'),
        # (r'/song/insert', 'handler.song.InsertHandler'),
        # (r'/song/del', 'handler.song.DelHandler'),
        # (r'/song/listtop', 'handler.song.ListTopHandler'),
        # (r'/song/mtone', 'handler.song.ToneHandler'),
        (r'/(.*\.txt)', StaticFileHandler, {'path': STATIC_PATH}),
     )
]
class Application(web.Application):

    def __init__(self):
        settings = {
            'login_url': '/login',
            'xsrf_cookies': False,
            'compress_response': True,
            'debug': options.debug,
            'ui_modules': uimodules,
            'ui_methods': uimethods,
            'static_path': STATIC_PATH,
            'template_path': os.path.join(sys.path[0], 'tpl'),
            'cookie_secret': base64.b64encode(uuid.uuid3(uuid.NAMESPACE_DNS, 'myktv').bytes),
            'sentry_url': 'https://d11a209bf6b44d108e21a1e4bf0a8c64:e8d0d661b78e48df81fa6f0e54248ae3@sentry.ktvsky.com/6'
        }
        web.Application.__init__(self, **settings)
        for spec in URLS:
            host = spec[0] if not options.debug else '.*$'
            handlers = spec[1:]
            self.add_handlers(host, handlers)


def run():
    app = Application()
    app.sentry_client = AsyncSentryClient(app.settings['sentry_url'])
    http_server = HTTPServer(app, xheaders=True)
    http_server.listen(options.port)
    print('Running on port %d' % options.port)
