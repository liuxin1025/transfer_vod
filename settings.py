#!/usr/bin/env python
# -*- coding: utf-8 -*-

# redis
REDIS = {
    'host': '10.10.155.122',
    'port': 6379
}

# mysql
DB_KTV = 'myktv'
MYSQL_KTV = {
    DB_KTV:{
        'master': {
            'host': '10.10.146.167',
            'user': 'ktvsky',
            'pass': '098f6bcd4621d373cade4e832627b4f6',
            'port': 3306
        },
        'slaves': [
            {
                'host': '10.10.168.41',
                'user': 'ktvsky',
                'pass': '098f6bcd4621d373cade4e832627b4f6',
                'port': 3308
            }
        ],
    },
}

# upyun
UPYUN = {
    'api': 'http://m0.api.upyun.com/',
    'bucket': 'autodynemv',
    'secret': '/6US86qn0tUQ/+oCAhjgO/nXv+w=',
    'cdn': 'http://autodynemv.b0.upaiyun.com',
    'username': 'guobin',
    'password': 'guobin@upyun.com',
    'url': 'https://cdn.ktvsky.com/'
}

ERR_MSG = {
    200: '服务正常',
    10001: '请求参数错误',
    10002: '请查收短信，稍后再试',
    10003: '验证码错误',
    10004: 'ktv已被其他代理商激活',
    10005: '您没有抽奖机会',
    10006: '活动没有在进行中',
    40004: '无数据',
    40001: '请先在发布平台配置ktv',
    40002: '操作不合法，购买/领取数量超过剩余数量',
    40004: '余额不足',
    50001: '系统错误',
}

# time
A_MINUTE = 60
A_HOUR = 3600
A_DAY = 24 * A_HOUR

# order_state
OrderState = {
    'CREATED': 0,         # 订单创建
    'UNPAY': 1,           # 订单未支付
    'PAYED': 2,           # 订单已支付
    'REVERSE': 3,         # 订单撤销
    'CLOSE': 4,           # 订单关闭
    'REFUNDING': 5,       # 订单退款申请
    'REFUNDED': 6,        # 订单退款成功
    'REFUND_FAIL': 7      # 订单退款失败
}

OrderStateString = {
    0: '订单创建',
    1: '订单未支付',
    2: '订单已支付',
    3: '订单撤销',
    4: '订单关闭',
    5: '订单退款申请',
    6: '订单退款成功',
    7: '订单退款失败'
}

PayType = {
    'wechat': '微信支付',
    'alipay': '支付宝支付',
    'pos': 'pos支付',
}

OrderActionString = {
    0: '双屏支付',
    1: '枪扫支付',
    2: '网页支付'
}

APIS = {
    'order_sum': 'http://pay.ktvsky.com/order/sum/{pay_type}/{ktv_id}',
    'wx_account_order': 'http://pay.ktvsky.com/account/wechat/{ktv_id}',
    'pos_account_order': 'http://pay.ktvsky.com/account/pos/{ktv_id}',
    'ali_account_order': 'http://pay.ktvsky.com/account/alipay/{ktv_id}',
    'withdraw_history': 'http://pay.ktvsky.com/withdraw/history/{ktv_id}',
    # 'account_history': 'http://pay.ktvsky.com/withdraw/history/{ktv_id}',
    'account_history': 'http://pay.ktvsky.com/account/income/{ktv_id}',
    'calc_withdraw': 'http://pay.ktvsky.com/account/income/{ktv_id}',
    'withdraw': 'http://pay.ktvsky.com/withdraw/{ktv_id}',
    'withdraw_account': 'http://pay.ktvsky.com/withdraw/account/{ktv_id}',
    'order': 'http://pay.ktvsky.com/order/{pay_type}',
    'ktv_pos': 'http://pay.ktvsky.com/ktv/pos/{ktv_id}',
    'bank': 'http://api.ktvsky.com/bank/{ktv_id}',
    'ktv_fin_curdata': 'http://{ktv_id}.ngrok.ktvsky.com/summary/{data_type}',
    'ktv_service_info':'http://open.ktv.api.ktvdaren.com/thundersir.aspx',
    'sub_ktv_service_info':'http://open.ktv.api.ktvdaren.com/thundersir.aspx'
}

CARDS_API_URLS = {
    'fetch_user_cards': 'http://{ktv_id}.ngrok.ktvsky.com/member/getmembercard?phone={phone}',
    'fetch_ktv_card_types': 'http://{ktv_id}.ngrok.ktvsky.com/member/getmembertype',
    'fetch_ktv_card_his': 'http://coupon.ktvsky.com/card/recharge/history/{ktv_id}',
    'create_ktv_card': 'http://{ktv_id}.ngrok.ktvsky.com/erp/member/membersendcard',
}

SECURET = 'LSKDFJA9LS5LKJO980DSJWL2NL234B03'
CAR_SECURET = 'SUPERCARA9LS5LKJO980DSJWL2NL234B'
MYKTV_SECRET = '8C8C3BA474004E78A706269D4D99E388'

AC_TASK_REWARD = 1
SP_TASK_REWARD = 1

# 雷石唱响
WX_CONF = {
    'appid': 'wx91ef6ff49f601368',
    'appsecret': '34484ddcb8ddb2ea14233405576389a5'
}

# 收银员等级
WX_SYY_CONF = {
    'appid': 'wx790c59cfd383eb60',
    'appsecret': '0086acb983365eb952fc37cd52ef4e83'
}

WXAPP = {
    'appid': 'wxe29de6e0fb0700ff',
    'appsecret': '5ddc333e05d6914a94743c82346768c6'
}

WX_GRANT_URL = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid={appid}&redirect_uri={redirect_uri}&response_type=code&scope={scope}&state={state}&connect_redirect=1#wechat_redirect'
WX_BASE_GRANT_URL = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid={appid}&redirect_uri={redirect_uri}&response_type=code&scope=snsapi_base&state={state}&connect_redirect=1#wechat_redirect'
WX_USERINFO_GRANT_URL = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid={appid}&redirect_uri={redirect_uri}&response_type=code&scope=snsapi_userinfo&state={state}&connect_redirect=1#wechat_redirect'
FETCH_OPENID_URL = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={appid}&secret={secret}&code={code}&grant_type=authorization_code'
FETCH_USERINFO_URL = 'https://api.weixin.qq.com/sns/userinfo?access_token={access_token}&openid={openid}&lang=zh_CN'
FETCH_USERINFO_URL_V2 = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token={access_token}&openid={openid}&lang=zh_CN'
WX_REDIRECT_URL = 'https://erp.ktvsky.com/wx'
QRCODE_TICKET = 'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token={access_token}'
TEMPLATE_MSG_URL = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}'

COMMON_URL = 'http://gm.ktvsky.3231266f50027675yg.custom.ucloud.cn'
COMMON_ORDER_URL = 'http://coupon.ktvsky.com/common/order?order_id={order_id}'
RED_PACK_TEMPLATE_ID = ''

NEW_TASK_REWARD=None
NEW_TASK = {
    'type': 'temp_task',   # 新增任务
    'title': None,
    'dst': None
}

LAKALA_CONF = {
    'DC_RATE': 0.0045,  # 借记卡费率
    'CC_RATE': 0.0055,  # 信用卡费率
    'WX_RATE': 0.003,  # 微信费率
    'ALI_RATE': 0.003,  # 支付宝费率
    #T+1
    'LS_DC_RATE_1': 0.005,
    'LS_CC_RATE_1': 0.006,
    'LS_WX_RATE_1': 0.005,
    'LS_ALI_RATE_1': 0.005,
    #T+7
    'LS_DC_RATE_7': 0.0048,
    'LS_CC_RATE_7': 0.0058,
    'LS_WX_RATE_7': 0.0048,
    'LS_ALI_RATE_7': 0.0048,
    #pos押金
    'DEPOSIT': 100000,
    'PUB_KEY_PATH': './pem/lakala/rsa_public_key.pem',
}
WX_RATE_DESC = '根据官方规则，提现成功后24小时到账'

ORDER_CHANNEL = {
    'wx': 0,
    'wechat': 0,
    'ali': 1,
    'alipay': 1,
    'pos': 2,
}
ORDER_TP = {
    'normal': [0, 3, 4, 5, 6, 7, 8],
    'zzh': [1, 2],
    'movie': [1],
    'red': [2],
}

BILL_TP = {
    'in': [0, 3, 5, 9],  # 入账
    'out': [1, 2, 4, 7, 8, 10],  # 出账
    'profit': [6],  # 收益
}

MCH_ACCOUNT_TYPE_NAME = [
    '营业收入', '提现', '加急手续费', '返还手续费', 'pos押金', '返还pos押金', '理财收益', '商城购买', '服务费', '补款', '补扣款'
]
MCH_ACCOUNT_TYPE = {
    'income': 0,
    'withdraw': 1,
    'fast_rate': 2,
    'return_rate': 3,
    'pos_deposit': 4,
    'return_pos_deposit': 5,
    'profit': 6,
    'market': 7,
    'service_charge': 8,
    'in_fee': 9,
    'out_fee': 10
}

ZZH_BILL_TP = {
    'in': [0],
    'out': [1, 2]
}
ZZH_ACCOUNT_TYPE_NAME = ['营业收入', '提现', '加急手续费']
ZZH_ACCOUNT_TYPE = {
    'income': 0,
    'withdraw': 1,
    'fast_rate': 2,
}

NEW_TEST_KTVS = []
FAST_RATE = 0.002

ERP_URL = 'http://{ktv_id}.ngrok.ktvsky.com/erp'

ERP_POS_URLS = {
    'getroomtopay': ERP_URL + '/room/getroomtopay',
    'getunpaidbills': ERP_URL + '/order/getunpaidbills',
    'getroombilldetail': ERP_URL + '/order/getroombilldetail',
    'getrecipebilldetail': ERP_URL + '/order/getrecipebilldetail',
    'paybills': ERP_URL + '/order/paybills',
}

# try to load debug settings
try:
    from tornado.options import options
    if options.debug:
        exec(compile(open('settings.debug.py')
             .read(), 'settings.debug.py', 'exec'))
except:
    pass
