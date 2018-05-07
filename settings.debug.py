#!/usr/bin/env python
# -*- coding: utf-8 -*-

REDIS = {
    'host': '127.0.0.1',
    'port': 6379
}

MYSQL_KTV['myktv']['slaves'] = []
MYSQL_KTV['myktv']['master'] = {
    'host': '192.168.0.172',
    'user': 'mombaby',
    'pass': '098f6bcd4621d373cade4e832627b4f6',
    'port': 3308
}

APIS = {
    'order_sum': 'http://pay.stage.ktvsky.com/order/sum/{pay_type}/{ktv_id}',
    'wx_account_order': 'http://pay.stage.ktvsky.com/account/wechat/{ktv_id}',
    'pos_account_order': 'http://pay.stage.ktvsky.com/account/pos/{ktv_id}',
    'ali_account_order': 'http://pay.stage.ktvsky.com/account/alipay/{ktv_id}',
    'withdraw_history': 'http://pay.stage.ktvsky.com/withdraw/history/{ktv_id}',
    # 'account_history': 'http://pay.stage.ktvsky.com/withdraw/history/{ktv_id}',
    'account_history': 'http://pay.stage.ktvsky.com/account/income/{ktv_id}',
    'calc_withdraw': 'http://pay.stage.ktvsky.com/account/income/{ktv_id}',
    'withdraw': 'http://pay.stage.ktvsky.com/withdraw/{ktv_id}',
    'withdraw_account': 'http://pay.stage.ktvsky.com/withdraw/account/{ktv_id}',
    'bank': 'http://api.stage.ktvsky.com/bank/{ktv_id}',
    'order': 'http://pay.stage.ktvsky.com/order/{pay_type}',
    'ktv_pos': 'http://pay.stage.ktvsky.com/ktv/pos/{ktv_id}',
    'ktv_fin_curdata': 'http://stub.stage.ktvsky.com/summary/{data_type}',
    'ktv_service_info': 'http://open.ktv.api.ktvdaren.com/thundersir.aspx',
    'sub_ktv_service_info': 'http://open.ktv.api.ktvdaren.com/thundersir.aspx'
}

CARDS_API_URLS = {
    'fetch_user_cards': 'http://{ktv_id}.ngrok.ktvsky.com/member/getmembercard?phone={phone}',
    'fetch_ktv_card_types': 'http://{ktv_id}.ngrok.ktvsky.com/member/getmembertype',
    'fetch_ktv_card_his': 'http://coupon.ktvsky.com/card/new/history/{ktv_id}',
    'create_ktv_card': 'http://{ktv_id}.ngrok.ktvsky.com/erp/member/membersendcard',
}

# 雷石唱响
WX_CONF = {
    'appid': 'fake appid',
    'appsecret': 'fake appsecret'
}
WX_REDIRECT_URL = 'https://erp.stage.ktvsky.com/wx'
COMMON_URL = 'http://common.stage.ktvsky.com'
RED_PACK_TEMPLATE_ID = 'MmRb8s__FhdvpNT0lXcatYueAtE1YnJM9gEw5hvDAsE'

WXAPP = {
    'appid': 'wx25a075ad055fefee',
    'appsecret': '38af54628f0ea2f2c2f31aeee1a8c32a'
}
