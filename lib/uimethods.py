#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from decimal import Decimal
from datetime import datetime, date
from settings import OrderActionString
from tornado.options import options

# def static_url(handler, path, include_host=None, **kwargs):
#     s_url = handler.static_url(path, include_host, *kwargs)
#     if options.debug:
#         return s_url
#     return 'http://erp.static.ktvsky.com/static/%s?v=%s'%(path, s_url.split('?v=')[1])

def datetime_str(handler, time_obj):
    return time_obj.strftime('%Y-%m-%d %H:%M:%S')

def json_format(handler, res):

    def _format(obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(obj, Decimal):
            return ('%.2f' % obj)
        if isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')

    return json.dumps(res, default=_format)

def order_action_to_text(handler, action):
    return OrderActionString.get(action, '不详')

def trim(handler, val, length, ellipsis='...', ret='before'):
    if val:
        if len(val) < length + 2:
            return val
        else:
            ellipsis = ellipsis if len(val) > length and ellipsis else ''
            split_str = val[:length] if ret == 'before' else val[length:]
            return split_str + ellipsis
    else:
        return ''

def date_time_to_date(handler, date_time):
    return datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S').date()

def is_expired(handler, dt):
    now = datetime.now().date()
    if isinstance(dt, datetime):
        return dt.date() < now
    elif isinstance(dt, str) and dt:
        fm = '%Y-%m-%d'
        if len(dt) > 10:
            fm = '%Y-%m-%d %X'
        return datetime.strptime(dt, fm).date() < now
    return False

def format_gzh_order_tp(handler, tp):
    if tp=='groupon':
        return '团购'
    elif tp=='buffet':
        return '自助餐'
    elif tp=='recipe':
        return '酒水'
    elif tp=='erproom':
        return '包房'
    return ''

def gzh_order_status(handler, gzh_order):
    if gzh_order.get('status'):
        return '已使用 %s'%gzh_order.get('update_time', '')
    if is_expired('', gzh_order.get('expire_time')):
        return '已过期 %s'%gzh_order.get('expire_time')
    return '未使用'

def gzh_order_tp(handler, tp):
    mp = {'buffet':'自助餐券',
        'groupon':'团购套餐',
        'erproom':'房台预订',
        'recipe':'酒水超市'}
    if tp in mp:
        return mp[tp]
