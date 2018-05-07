#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import Column, or_, and_
from sqlalchemy.sql.expression import func, desc, asc
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, TINYINT, DATETIME, TIMESTAMP, DATE, DECIMAL

from settings import DB_KTV, OrderState
from mysql.base import NotNullColumn, Base
from lib.decorator import model_to_dict, filter_update_data, models_to_list, model2dict
import control
import logging



class KtvWx(Base):
    __tablename__ = 'ktv_wx'

    id = Column(INTEGER(11), primary_key=True)
    ktv_id = NotNullColumn(INTEGER(11))
    dogname = NotNullColumn(VARCHAR(128))
    appid= NotNullColumn(VARCHAR(32))
    appsecret = NotNullColumn(VARCHAR(32))
    order_tpid = NotNullColumn(VARCHAR(64))
    buy_card_tpid = NotNullColumn(VARCHAR(64))
    recharge_card_tpid = NotNullColumn(VARCHAR(64))
    card_order_tpid = NotNullColumn(VARCHAR(64))
    store_wine_tpid = NotNullColumn(VARCHAR(64))
    store_wine_expire_tpid = NotNullColumn(VARCHAR(64))
    redeem_tpid = NotNullColumn(VARCHAR(64))
    upgrade_card_tpid = NotNullColumn(VARCHAR(64))
    fetch_wine_tpid = NotNullColumn(VARCHAR(64))
    pre_order_tpid = NotNullColumn(VARCHAR(64))
    birthday_notify_tpid = NotNullColumn(VARCHAR(64))
    silent_user_tpid = NotNullColumn(VARCHAR(64))
    birthday_bless_tpid = NotNullColumn(VARCHAR(64))


class Cashier(Base):
    __tablename__ = 'cashier'

    cashier_id = Column(INTEGER(11), primary_key=True)
    nickname = NotNullColumn(VARCHAR(64), default='')
    headimgurl = NotNullColumn(VARCHAR(512), default='')
    ktv_id = NotNullColumn(INTEGER(11))
    client_id = NotNullColumn(INTEGER(11))
    openid = NotNullColumn(VARCHAR(64), default='')
    total_cash = NotNullColumn(INTEGER(11), default=0)
    score = NotNullColumn(INTEGER(11), default=0)
    ac_task = NotNullColumn(VARCHAR(64), default='0, 0')
    sp_task = NotNullColumn(VARCHAR(64), default='0, 0')
    info = NotNullColumn(VARCHAR(64), default='')


class CashierWithdraw(Base):
    __tablename__ = 'cashier_withdraw'

    withdraw_id = Column(INTEGER(11), primary_key=True)
    openid = NotNullColumn(VARCHAR(64))
    withdraw_money = NotNullColumn(INTEGER(11))


class KtvFinanceAccount(Base):
    __tablename__ = 'ktv_finance_account'

    id = Column(INTEGER(11), primary_key=True)
    ktv_id = NotNullColumn(INTEGER(11), default=0)
    username = NotNullColumn(INTEGER(11), default=0)
    password_org = NotNullColumn(VARCHAR(32), default='')
    password = NotNullColumn(VARCHAR(32), default='')


class ServiceInfo(Base):
    __tablename__ = 'ktv_service_info'

    id = Column(INTEGER(11),primary_key=True)
    ktv_id = NotNullColumn(INTEGER(11),default=0)
    ser_fee = NotNullColumn(INTEGER(11))
    ser_period = NotNullColumn(INTEGER(11))
    invoice = NotNullColumn(TINYINT(1),default=0)
    phone_num = NotNullColumn(VARCHAR(11),default='')
    contract_period= NotNullColumn(INTEGER(5), default=0)
    pay_cycle = NotNullColumn(INTEGER(5), default=0)
    month_price = NotNullColumn(INTEGER(5), default=0)
    auth_endtime = NotNullColumn(DATETIME, default=func.now())
    pay_mode = NotNullColumn(TINYINT(1), default=0)
    room_count = NotNullColumn(INTEGER(5), default=0)


class WxOrder(Base):
    __tablename__ = 'weixin_erp_order'

    id = Column(INTEGER(11), primary_key=True)
    order_id = NotNullColumn(VARCHAR(32))
    origin_oid = NotNullColumn(VARCHAR(32))
    ktv_id = NotNullColumn(INTEGER(11))
    wx_pay_id = NotNullColumn(VARCHAR(128))
    erp_id = NotNullColumn(VARCHAR(128))
    erp_date = NotNullColumn(DATETIME, default=func.now())
    total_fee = NotNullColumn(INTEGER)
    body = NotNullColumn(VARCHAR(128)) # 商品详情
    remark = NotNullColumn(VARCHAR(128))
    other = NotNullColumn(VARCHAR(128))
    dogname = NotNullColumn(VARCHAR(128)) # 加密狗名称
    action = NotNullColumn(INTEGER) # 支付方式，0扫描 1刷卡(被扫码)
    format_product = NotNullColumn(VARCHAR(128), default='')
    coupon_fee = NotNullColumn(INTEGER(11), default=0)
    rate_fee = NotNullColumn(INTEGER(11), default=0)
    rt_rate_fee = NotNullColumn(INTEGER(11), default=0) # 返还手续费
    state = NotNullColumn(INTEGER) # 订单状态
    tp = NotNullColumn(INTEGER) # 业务类型 (0:普通 1:电影 2:红包)
    finish_time = NotNullColumn(DATETIME, default=func.now())
    openid = NotNullColumn(VARCHAR(64))
    c_openid = NotNullColumn(VARCHAR(64))


class AliOrder(Base):
    __tablename__ = 'ali_erp_order'

    id = Column(INTEGER(11), primary_key=True)
    order_id = NotNullColumn(VARCHAR(32))
    alipay_user_id = NotNullColumn(VARCHAR(64))
    coupon_send_id = NotNullColumn(VARCHAR(64))
    origin_oid = NotNullColumn(VARCHAR(32))
    ktv_id = NotNullColumn(INTEGER(11))
    ali_pay_id = NotNullColumn(VARCHAR(128))
    erp_id = NotNullColumn(VARCHAR(128)) # 线下订单号
    erp_date = NotNullColumn(DATETIME, default=func.now())
    total_fee = NotNullColumn(INTEGER)
    body = NotNullColumn(VARCHAR(128)) # 商品详情
    remark = NotNullColumn(VARCHAR(128)) #
    other = NotNullColumn(VARCHAR(128)) #
    dogname = NotNullColumn(VARCHAR(128)) # 加密狗名称
    action = NotNullColumn(INTEGER) # 支付方式，0扫描 1刷卡(被扫码)
    rate_fee = NotNullColumn(INTEGER(11), default=0)
    state = NotNullColumn(INTEGER) # 订单状态
    tp = NotNullColumn(INTEGER) # 业务类型 (0:普通 1:电影 2:红包)
    finish_time = NotNullColumn(DATETIME, default=func.now())


class PosOrder(Base):
    __tablename__ = 'pos_order'

    order_id = Column(INTEGER(11), primary_key=True)
    ktv_id = NotNullColumn(INTEGER(11)) # 歌厅ID
    amount = NotNullColumn(INTEGER(11)) # 金额
    term_id = NotNullColumn(VARCHAR(32)) # POS终端号
    merchant_id = NotNullColumn(VARCHAR(32)) # 平台商户号
    pay_type = NotNullColumn(TINYINT(1)) # 0:银行卡 1:微信 2:支付宝
    term_serno = NotNullColumn(VARCHAR(32)) # 终端流水号
    order_no = NotNullColumn(VARCHAR(32)) # 订单编号
    rate_fee = NotNullColumn(INTEGER(11)) # 订单手续费
    rt_rate_fee = NotNullColumn(INTEGER(11), default=0) # 返还手续费
    state = NotNullColumn(TINYINT(1)) # 交易结果
    finish_time = NotNullColumn(DATETIME, default=func.now())

    orderid_scan = NotNullColumn(VARCHAR(32))  # 扫码订单号 (微信,支付宝扫码支付订单号)
    batchbillno = NotNullColumn(VARCHAR(32))  # 批次号
    systraceno = NotNullColumn(VARCHAR(32))  # 凭证号
    bank_type = NotNullColumn(VARCHAR(16))
    err_code = NotNullColumn(VARCHAR(32))  # 错误代码
    pos_rate_fee = NotNullColumn(INTEGER(11))  # pos手续费


class Pos(Base):
    __tablename__ = 'pos'

    id = Column(INTEGER(11), primary_key=True)
    term_id = NotNullColumn(VARCHAR(32)) # POS终端号
    ktv_id = NotNullColumn(INTEGER(11)) # 歌厅ID


class ArchiveOrder(Base):
    '''
    订单归档表
    '''
    __tablename__ = 'archive_order'

    id = Column(INTEGER(11), primary_key=True)
    order_id = NotNullColumn(VARCHAR(32))
    erp_id = NotNullColumn(VARCHAR(128))
    ktv_id = NotNullColumn(INTEGER(11))
    total_fee = NotNullColumn(INTEGER(11), default=0)
    ch_rate_fee = NotNullColumn(INTEGER(11), default=0) #渠道手续费
    ls_rate_fee = NotNullColumn(INTEGER(11), default=0) #雷石手续费
    channel = NotNullColumn(INTEGER) # 渠道类型 (0:微信 1:支付宝 2:pos)
    tp = NotNullColumn(INTEGER) # 业务类型 (0:普通 1:电影 2:红包)
    state = NotNullColumn(INTEGER) # 订单状态
    finish_time = NotNullColumn(DATETIME, default=func.now())
    body = NotNullColumn(VARCHAR(128))  # 商品详情
    income_id = NotNullColumn(INTEGER(11))

    #pos
    term_id = NotNullColumn(VARCHAR(32))  # 终端号
    card_no = NotNullColumn(VARCHAR(32))  # 交易卡号
    pos_type = NotNullColumn(TINYINT(1))  # pos交易类型 0:借记卡 1:微信 2:支付宝 3:贷记卡


class MchFinancial(Base):
    '''
    商户收益表
    '''
    __tablename__ = 'mch_financial'

    id = Column(INTEGER(11), primary_key=True)
    ktv_id = NotNullColumn(INTEGER(11))

    principal = NotNullColumn(INTEGER(11), default=0) # 本金
    profit = NotNullColumn(INTEGER(11), default=0) # 收益
    rate = NotNullColumn(DECIMAL(10, 7)) # 收益率
    date = NotNullColumn(DATE) # 本金所在日期


class MchIncome(Base):
    '''
    商户营收表
    '''
    __tablename__ = 'mch_income'

    id = Column(INTEGER(11), primary_key=True)
    ktv_id = NotNullColumn(INTEGER(11))
    # 普通业务
    normal_fee = NotNullColumn(INTEGER(11), default=0)
    normal_rate = NotNullColumn(INTEGER(11), default=0)
    # 增值业务
    zzh_fee = NotNullColumn(INTEGER(11), default=0)
    zzh_rate = NotNullColumn(INTEGER(11), default=0)

    state = NotNullColumn(INTEGER)  # 结算状态 0结算中 1已结算
    start_time = NotNullColumn(DATETIME)
    end_time = NotNullColumn(DATETIME)
    pos_start_time = NotNullColumn(DATETIME)
    pos_end_time = NotNullColumn(DATETIME)
    date = NotNullColumn(DATE)


class MchAccount(Base):
    '''
    账户表
    '''
    __tablename__ = 'mch_account'

    id = Column(INTEGER(11), primary_key=True)
    ktv_id = NotNullColumn(INTEGER(11))

    money = NotNullColumn(INTEGER(11), default=0)
    balance = NotNullColumn(INTEGER(11), default=0) #余额
    type = NotNullColumn(INTEGER) # 0:营收 1:提现 2:加急手续费 3:返还手续费 4:pos押金 5:pos押金返还 6:收益
    state = NotNullColumn(INTEGER) # 0:处理中 1:已完成
    detail = NotNullColumn(VARCHAR(1024))
    end_date = NotNullColumn(DATE)
    finish_time = NotNullColumn(TIMESTAMP)
    ktype = NotNullColumn(INTEGER)


class ZzhAccount(Base):
    '''
    增值账户表 (电影红包)
    '''
    __tablename__ = 'zzh_account'

    id = Column(INTEGER(11), primary_key=True)
    ktv_id = NotNullColumn(INTEGER(11))

    money = NotNullColumn(INTEGER(11), default=0)
    balance = NotNullColumn(INTEGER(11), default=0) #余额
    type = NotNullColumn(INTEGER) # 0:营收 1:提现 2:加急手续费
    state = NotNullColumn(INTEGER) # 0:处理中 1:已完成
    detail = NotNullColumn(VARCHAR(1024))
    end_date = NotNullColumn(DATE)
    finish_time = NotNullColumn(TIMESTAMP)

class MarketCartItem(Base):
    '''
    购物车
    '''
    __tablename__ = 'market_cart_item'

    id = Column(INTEGER(11), primary_key=True)
    ktv_id = NotNullColumn(INTEGER(11), default=0)
    product_item_id = NotNullColumn(INTEGER(11), default=0)
    num = NotNullColumn(INTEGER(11), default=0)
    is_true = NotNullColumn(TINYINT(1))


class MarketProduct(Base):
    '''
    商品概述表
    '''

    __tablename__ = 'market_product'

    id = Column(INTEGER(11), primary_key=True)
    name = NotNullColumn(VARCHAR(128), default='')  # 商品名称
    price = NotNullColumn(VARCHAR(128), default='')
    freight = NotNullColumn(VARCHAR(128), default='')    # 运费区间
    params = NotNullColumn(VARCHAR(256), default='')    # 参数1({"name": "颜色", "value": "["红色", "蓝色", "绿色"]"})
    details_img = NotNullColumn(VARCHAR(128), default='')   # 商品详情
    main_img = NotNullColumn(VARCHAR(128), default='')  # 商品主图
    tg_img = NotNullColumn(VARCHAR(128), default='')  # 推广图
    row = NotNullColumn(INTEGER(11), default=0)    # 商品展示位置:行(0:不展示)
    col = NotNullColumn(INTEGER(11), default=0)   # 商品展示位置:列(0:不展示)
    class_1 = NotNullColumn(INTEGER(11), default=0)    # 商品一级分类
    class_2 = NotNullColumn(INTEGER(11), default=0)    # 商品二级分类
    is_tg = NotNullColumn(INTEGER)  # 是否推广
    is_try = NotNullColumn(INTEGER)  # 是否试用
    buy_object = NotNullColumn(INTEGER)  # 购买对象 0:所有 1:使用微信和支付宝的商户可购买 2:使用pos机的商户可购买
    not_buy_remark = NotNullColumn(VARCHAR(512), default='')   # 无法购买说明
    remark = NotNullColumn(VARCHAR(512), default='')   # 说明

class MarketProductItem(Base):
    '''
    实际商品表
    '''
    __tablename__ = 'market_product_item'

    id = Column(INTEGER(11), primary_key=True)
    product_id = NotNullColumn(INTEGER(11), default=0)  # MarketProduct.id
    name = NotNullColumn(VARCHAR(128), default='')  # 商品名称
    price = NotNullColumn(INTEGER(11), default=0)   # 商品价格
    freight = NotNullColumn(INTEGER(11), default=0)   # 运费
    spec = NotNullColumn(VARCHAR(128), default='')   # 商品规格("红色/1.6L")
    imgs = NotNullColumn(VARCHAR(512), default='')  # 商品图片组
    num = NotNullColumn(INTEGER(11), default=0)    # 库存
    try_num = NotNullColumn(INTEGER(11), default=0)    # 试用数量
    buy_num = NotNullColumn(INTEGER(11), default=0)    # 销量
    min_num = NotNullColumn(INTEGER(11), default=0)    # 最小购买数量
    max_num = NotNullColumn(INTEGER(11), default=0)    # 最大购买数量


class MarketAddress(Base):
    '''
    收货地址
    '''

    __tablename__ = 'market_address'

    id = Column(INTEGER(11), primary_key=True)
    ktv_id = NotNullColumn(INTEGER(11), default=0)
    name = NotNullColumn(VARCHAR(128), default='')
    phone = NotNullColumn(VARCHAR(11), default='')
    details = NotNullColumn(VARCHAR(512), default='')


class MarketOrder(Base):
    '''
    订单表
    '''

    __tablename__ = 'market_order'

    id = Column(INTEGER(11), primary_key=True)
    ktv_id = NotNullColumn(INTEGER(11), default=0)
    buy_items = NotNullColumn(VARCHAR(1024), default='')
    money = NotNullColumn(INTEGER(11), default=0)
    freight = NotNullColumn(INTEGER(11), default=0)   # 运费
    logistics = NotNullColumn(VARCHAR(128), default='')  # 物流信息
    address = NotNullColumn(VARCHAR(512), default='')  # 收货地址
    state = NotNullColumn(INTEGER) # 0:待付款 1:待发货 2:待收货 3:完成



class WxWithdraw(Base):
    __tablename__ = 'weixin_erp_withdraw'

    id = Column(INTEGER(11), primary_key=True)
    ktv_id = NotNullColumn(INTEGER(11))
    withdraw_money = NotNullColumn(INTEGER(11), default=0) # 微信结算
    service_charge = NotNullColumn(INTEGER(11), default=0) # 微信结算手续费
    ali_withdraw_money = NotNullColumn(INTEGER(11), default=0)
    ali_service_charge = NotNullColumn(INTEGER(11), default=0)
    pos_withdraw_money = NotNullColumn(INTEGER(11), default=0)
    pos_service_charge = NotNullColumn(INTEGER(11), default=0)
    other_withdraw_money = NotNullColumn(INTEGER(11), default=0) # 增值业务(电影,红包)
    other_service_charge = NotNullColumn(INTEGER(11), default=0)

    account_money = NotNullColumn(INTEGER(11), default=0) # 结算总金额(扣除手续费)
    fast_rate = NotNullColumn(INTEGER(11), default=0) # 加急手续费
    start_date = NotNullColumn(TIMESTAMP)
    end_date = NotNullColumn(TIMESTAMP)
    date = NotNullColumn(VARCHAR(16))
    state = NotNullColumn(INTEGER) # 结算状态 0结算中 1已结算

    return_service_charge = NotNullColumn(INTEGER(11), default=0)


class KtvAccount(Base):
    __tablename__ = 'ktv_account'

    id = Column(INTEGER(11), primary_key=True)
    ktv_id = NotNullColumn(INTEGER(11))
    tp = NotNullColumn(INTEGER) # 提现类型, 0提现, 1购买服务费 等
    withdraw_id = NotNullColumn(VARCHAR(128)) # 每笔提现保证唯一,通过保证不重复提现
    withdraw_money = NotNullColumn(INTEGER(11), default=0)
    account_money = NotNullColumn(INTEGER(11), default=0) # 账户总金额(扣除手续费, 处理完当前提现后的剩余费用)
    bank_account = NotNullColumn(VARCHAR(32)) # 银行账号
    bank_name = NotNullColumn(VARCHAR(32)) # 银行名字
    bank_branch = NotNullColumn(VARCHAR(128)) # 开户支行名字
    account_name = NotNullColumn(VARCHAR(128)) # 银行账号户名
    state = NotNullColumn(INTEGER) # 提现单状态 0处理中 1已完成 2拒绝
    finish_time = NotNullColumn(TIMESTAMP) # 财务打款完成时间
    end_date = NotNullColumn(TIMESTAMP)


class KtvAgent(Base):
    __tablename__ = 'ktv_agent'

    id = Column(INTEGER(11), primary_key=True)
    openid = NotNullColumn(VARCHAR(64))
    name = NotNullColumn(VARCHAR(64), default='')
    province_id = NotNullColumn(INTEGER(11), default=0)
    city_id = NotNullColumn(INTEGER(11), default=0)
    phone_num = NotNullColumn(VARCHAR(11), default='')
    email = NotNullColumn(VARCHAR(128), default='')
    payed = NotNullColumn(TINYINT(1), default=0)
    order_id = NotNullColumn(VARCHAR(128))
    wx_pay_id = NotNullColumn(VARCHAR(128))
    fee = NotNullColumn(INTEGER(11))
    password_org = NotNullColumn(VARCHAR(11), default='')
    password = NotNullColumn(VARCHAR(32), default='')


class GzhLotteryActivity(Base):
    __tablename__ = 'gzh_lottery_activity'

    id  = Column(INTEGER(11), primary_key=True)
    ktv_id = Column(INTEGER(11))
    start_time = Column(DATETIME)
    end_time = Column(DATETIME)
    status = Column(TINYINT(1))
    rules = Column(VARCHAR(1024))


class GzhLottery(Base):
    __tablename__ = 'gzh_lottery'

    id = Column(INTEGER(11), primary_key=True)
    ktv_id = Column(INTEGER(11), default=0)
    name = Column(VARCHAR(128), default='')
    count = Column(INTEGER(11), default=0)
    image = Column(VARCHAR(1024), default='')
    min_fee = Column(INTEGER(11))
    percent = Column(VARCHAR(16), default='')


class GzhLotteryRecord(Base):
    __tablename__ = 'gzh_lottery_record'

    id = Column(INTEGER(11), primary_key=True)
    ktv_id = Column(INTEGER(11), default=0)
    lottery_id = Column(INTEGER(11), default=0)
    code = Column(VARCHAR(11), default='')
    status = Column(TINYINT(1), default=0)
    openid = NotNullColumn(VARCHAR(64))


class CustomKtv(Base):
    __tablename__ = 'custom_ktv'

    id = Column(INTEGER(11), primary_key=True)
    agent_openid = NotNullColumn(INTEGER(11))
    ktv_id = NotNullColumn(INTEGER(11))
    ktv_name = NotNullColumn(VARCHAR(128))
    status = NotNullColumn(TINYINT(1))


class CustomKtvOrder(Base):
    __tablename__ = 'custom_ktv_order'

    id = Column(INTEGER(11), primary_key=True)
    custom_ktv_id = NotNullColumn(INTEGER(11))
    order_id = NotNullColumn(VARCHAR(128))
    wx_pay_id = NotNullColumn(VARCHAR(128))
    years = NotNullColumn(TINYINT(1))
    push_years = NotNullColumn(TINYINT(1))
    fee = NotNullColumn(INTEGER(11))
    state = NotNullColumn(TINYINT(1)) # 订单状态


class GzhBuffet(Base):
    __tablename__ = 'gzh_buffet'

    id = Column(INTEGER(11), primary_key=True)
    ktv_id = NotNullColumn(INTEGER(11))
    image = NotNullColumn(VARCHAR(128))
    name = NotNullColumn(VARCHAR(128))
    detail = NotNullColumn(VARCHAR(128))
    presell = NotNullColumn(INTEGER(11))
    price = NotNullColumn(INTEGER(11))
    discount_price = NotNullColumn(INTEGER(11))
    count = NotNullColumn(INTEGER(11))
    left = NotNullColumn(INTEGER(11))
    lunch_time = NotNullColumn(VARCHAR(64))
    status = NotNullColumn(TINYINT(1))


class GzhGroupon(Base):
    __tablename__ = 'gzh_groupon'

    id = Column(INTEGER(11), primary_key=True)
    ktv_id = NotNullColumn(INTEGER(11))
    image = NotNullColumn(VARCHAR(128))
    name = NotNullColumn(VARCHAR(128))
    detail = NotNullColumn(VARCHAR(128))
    expire = NotNullColumn(DATETIME)
    price = NotNullColumn(INTEGER(11))
    discount_price = NotNullColumn(INTEGER(11))
    count = NotNullColumn(INTEGER(11))
    left = NotNullColumn(INTEGER(11))
    status = NotNullColumn(TINYINT(1))


class GzhUserCoupon(Base):
    __tablename__ = 'gzh_user_coupon'

    id = Column(INTEGER(11), primary_key=True)
    ktv_id = NotNullColumn(INTEGER(11))
    openid = NotNullColumn(VARCHAR(64))
    tp = NotNullColumn(VARCHAR(32))
    coupon_id = NotNullColumn(INTEGER(11))
    expire_time = NotNullColumn(DATETIME)
    status = NotNullColumn(TINYINT(1))


class GzhUser(Base):
    __tablename__ = 'gzh_user'

    id = Column(INTEGER(11), primary_key=True)
    ktv_id = NotNullColumn(INTEGER(11))
    openid = NotNullColumn(VARCHAR(64), default='')
    headimgurl = NotNullColumn(VARCHAR(512), default='')
    nickname = NotNullColumn(VARCHAR(128), default='')
    user_name = NotNullColumn(VARCHAR(64))
    phone_num = NotNullColumn(VARCHAR(11))
    flag = NotNullColumn(TINYINT(1), default=0)
    earn_sum = NotNullColumn(INTEGER(11))


class GzhOrder(Base):
    __tablename__ = 'gzh_order'

    id = Column(INTEGER(11), primary_key=True)
    openid = NotNullColumn(VARCHAR(64))
    ktv_id = NotNullColumn(INTEGER(11))
    order_id = NotNullColumn(VARCHAR(32))
    wx_pay_id = NotNullColumn(VARCHAR(128))
    state = NotNullColumn(TINYINT(1))
    total_fee = NotNullColumn(INTEGER(11))
    vip_total_fee = NotNullColumn(INTEGER(11))
    pay_fee = NotNullColumn(INTEGER(11))
    tp=NotNullColumn(VARCHAR(11))
    detail = NotNullColumn(VARCHAR(4096))
    user_name = NotNullColumn(VARCHAR(64))
    phone_num = NotNullColumn(VARCHAR(11))
    expire_time = NotNullColumn(DATETIME)
    status = NotNullColumn(TINYINT(1))
    remarked = NotNullColumn(TINYINT(1))
    paytype= NotNullColumn(TINYINT(1), default=1)
    room_num = NotNullColumn(VARCHAR(128))
    remarks = NotNullColumn(VARCHAR(1024))
    lottery = NotNullColumn(TINYINT(1))
    printed = NotNullColumn(TINYINT(1))
    vip_card_info = NotNullColumn(VARCHAR(512))


class GzhRemark(Base):
    __tablename__ = 'gzh_remark'

    id = Column(INTEGER(11), primary_key=True)
    nickname = NotNullColumn(VARCHAR(128), default='')
    headimgurl = NotNullColumn(VARCHAR(512), default='')
    ktv_id = NotNullColumn(INTEGER(11))
    order_id = NotNullColumn(VARCHAR(32))
    grade = NotNullColumn(TINYINT(1))
    remark = NotNullColumn(VARCHAR(4096))
    status = NotNullColumn(TINYINT(1))
    remark_images = NotNullColumn(VARCHAR(4096))


class GzhDisOrder(Base):
    __tablename__ = 'gzh_dis_order'

    id = Column(INTEGER(11), primary_key=True)
    order_id = NotNullColumn(VARCHAR(32))
    openid = NotNullColumn(VARCHAR(64))
    phone_num = NotNullColumn(INTEGER(11))
    s_openid = NotNullColumn(VARCHAR(64))
    ktv_id = NotNullColumn(INTEGER(11))
    card_type = NotNullColumn(INTEGER(11))
    total_fee = NotNullColumn(INTEGER(11))
    payed = NotNullColumn(TINYINT(1))
    status = NotNullColumn(TINYINT(1))


class CardMember(Base):
    __tablename__ = 'card_member'

    id = Column(INTEGER(11), primary_key=True)
    openid = NotNullColumn(VARCHAR(64), default='')
    phone_num = NotNullColumn(VARCHAR(11), default='')
    ktv_id = NotNullColumn(INTEGER(11), default=0)
    zktv_id = NotNullColumn(INTEGER(11) , default=0)


class CardOrder(Base):
    __tablename__ = 'card_order'

    id = Column(INTEGER(11), primary_key=True)
    ktv_id = Column(INTEGER(11), default=0)
    zktv_id = Column(INTEGER(11), default=0)
    openid = Column(VARCHAR(64), default='')
    cards = Column(VARCHAR(512), default='')
    order_type = Column(TINYINT(1), default=0)
    state = Column(TINYINT(1), default=0)
    order_id = Column(VARCHAR(128), default='')
    wx_pay_id = Column(VARCHAR(128), default='')
    fee = Column(INTEGER(11), default=0)


class APIModel(object):

    def __init__(self, pdb):
        self.pdb = pdb
        self.master = pdb.get_session(DB_KTV, master=True)
        self.slave = pdb.get_session(DB_KTV)

    @model_to_dict
    def add_table(self, tb, **kwargs):
        try:
            one = eval(tb)(**kwargs)
            self.master.add(one)
            self.master.commit()
            return one
        except Exception as e:
            logging.info(e)
            self.master.rollback()

    @model_to_dict
    def get_cashier(self, ktv_id=None, client_id=None, openid=None):
        q = self.slave.query(Cashier)
        if ktv_id and client_id:
            q = q.filter_by(ktv_id=ktv_id).filter_by(client_id=client_id)
            q = q.order_by(Cashier.update_time.desc()).limit(1)
        if openid:
            q = q.filter_by(openid=openid)
        return q.scalar()

    @filter_update_data
    def update_cashier(self, openid, data):
        self.master.query(Cashier).filter_by(openid=openid).update(data)
        self.master.commit()

    @model_to_dict
    def add_cashier(self, **data):
        cashier = Cashier(**data)
        self.master.add(cashier)
        self.master.commit()
        return cashier

    def cal_withdraw_sum(self, openid):
        q = self.slave.query(func.sum(CashierWithdraw.withdraw_money).label('withdraw_money')).filter_by(openid=openid)
        return q.scalar() or 0

    @model_to_dict
    def add_cashier_withdraw(self, **data):
        cashier_withdraw = CashierWithdraw(**data)
        self.master.add(cashier_withdraw)
        self.master.commit()
        return cashier_withdraw

    @model_to_dict
    def get_ktv_fin_account(self, username):
        return self.slave.query(KtvFinanceAccount).filter_by(username=username).scalar()

    @model_to_dict
    def get_ktv_fin_account_from_ktv_id(self, ktv_id):
        return self.slave.query(KtvFinanceAccount).filter_by(ktv_id=ktv_id).first()

    def update_ktv_fin_account(self, **data):
        q = self.master.query(KtvFinanceAccount).filter_by(username=data['username'])
        if q.scalar():
            q.update(data)
        else:
            self.master.add(KtvFinanceAccount(**data))
        self.master.commit()

    @model_to_dict
    def insert_ser_info(self, **params):
        self.master.add(ServiceInfo(**params))
        self.master.commit()
        return ServiceInfo(**params)

    @model_to_dict
    def get_ktv_ser_order(self, tradeno):
        return self.slave.query(ServiceInfo).filter_by(id=tradeno).scalar()

    '''ArchiveOrder'''
    def update_archive_orders(self, ktv_id=None, channel=None, tp=None, start_time=None, end_time=None, data=None, income_id=None):
        q = self.master.query(ArchiveOrder)
        if ktv_id is not None:
            q = q.filter(ArchiveOrder.ktv_id == ktv_id)
        if channel is not None:
            q = q.filter(ArchiveOrder.channel == channel)
        if start_time is not None:
            q = q.filter(ArchiveOrder.finish_time >= start_time)
        if end_time is not None:
            q = q.filter(ArchiveOrder.finish_time <= end_time)
        if tp is not None:
            q = q.filter(ArchiveOrder.tp == tp)
        if income_id is not None:
            q = q.filter(ArchiveOrder.income_id == income_id)
        q.update(data)
        self.master.commit()

    def get_archive_order_sum(self, ktv_id=None, channel=None, tp=None, start_time=None, end_time=None, income_id=None):
        q = self.slave.query(ArchiveOrder.state, func.sum(ArchiveOrder.total_fee).label('total_fee'), func.sum(ArchiveOrder.ls_rate_fee).label('rate_fee'))
        if ktv_id is not None:
            q = q.filter(ArchiveOrder.ktv_id == ktv_id)
        if income_id is not None:
            q = q.filter(ArchiveOrder.income_id == income_id)
        if channel is not None:
            q = q.filter(ArchiveOrder.channel == channel)
        if tp is not None:
            q = q.filter(ArchiveOrder.tp.in_(tp))
        if start_time is not None:
            q = q.filter(ArchiveOrder.finish_time >= start_time)
        if end_time is not None:
            q = q.filter(ArchiveOrder.finish_time <= end_time)
        res = q.group_by(ArchiveOrder.state).all()
        pay_fee, pay_rate, refound_fee, refound_rate = 0, 0, 0, 0
        for item in res:
            if item.state == OrderState['PAYED']:
                pay_fee = item.total_fee
                pay_rate = item.rate_fee
            elif item.state == OrderState['REFUNDED']:
                refound_fee = item.total_fee
                refound_rate = item.rate_fee
        return int(pay_fee - abs(refound_fee)), int(pay_rate - refound_rate)

    def get_archive_order_count(self, ktv_id=None, channel=None, tp=None, start_time=None, end_time=None, income_id=None):
        q = self.slave.query(func.count('1')).filter(ArchiveOrder.state == 2)
        if ktv_id is not None:
            q = q.filter(ArchiveOrder.ktv_id == ktv_id)
        if income_id is not None:
            q = q.filter(ArchiveOrder.income_id == income_id)
        if channel is not None:
            q = q.filter(ArchiveOrder.channel == channel)
        if tp is not None:
            q = q.filter(ArchiveOrder.tp.in_(tp))
        if start_time is not None:
            q = q.filter(ArchiveOrder.finish_time >= start_time)
        if end_time is not None:
            q = q.filter(ArchiveOrder.finish_time <= end_time)
        count = q.scalar()
        return count

    @model_to_dict
    def get_archive_order(self, order_id):
        return self.slave.query(ArchiveOrder).filter_by(order_id=order_id).scalar()

    # @models_to_list
    def get_archive_orders(self, ktv_id=None, channel=None, tp=None, start_time=None, end_time=None, sort=None, page=None, page_size=None, income_id=None, term_id=None):
        q = self.slave.query(ArchiveOrder).filter(ArchiveOrder.state.in_([2, 6]))
        if ktv_id is not None:
            q = q.filter(ArchiveOrder.ktv_id == ktv_id)
        if income_id is not None:
            q = q.filter(ArchiveOrder.income_id == income_id)
        if channel is not None:
            q = q.filter(ArchiveOrder.channel == channel)
        if tp is not None:
            q = q.filter(ArchiveOrder.tp.in_(tp))
        if start_time is not None:
            q = q.filter(ArchiveOrder.finish_time >= start_time)
        if end_time is not None:
            q = q.filter(ArchiveOrder.finish_time <= end_time)
        if term_id is not None:
            q = q.filter(ArchiveOrder.term_id == term_id)
        if sort == 'asc':
            q = q.order_by(asc(ArchiveOrder.finish_time))
        else:
            q = q.order_by(desc(ArchiveOrder.finish_time))
        if page is not None and page_size is not None:
            q = q.offset((page - 1) * page_size).limit(page_size)
        return q.all()

    def get_m_archive_orders(self, ktv_id=None, channel=None, tp=None, start_time=None, end_time=None, sort=None, page=None, page_size=None, income_id=None):
        q = self.master.query(ArchiveOrder).filter(ArchiveOrder.state.in_([2, 6]))
        if ktv_id is not None:
            q = q.filter(ArchiveOrder.ktv_id == ktv_id)
        if income_id is not None:
            q = q.filter(ArchiveOrder.income_id == income_id)
        if channel is not None:
            q = q.filter(ArchiveOrder.channel == channel)
        if tp is not None:
            q = q.filter(ArchiveOrder.tp.in_(tp))
        if start_time is not None:
            q = q.filter(ArchiveOrder.finish_time >= start_time)
        if end_time is not None:
            q = q.filter(ArchiveOrder.finish_time <= end_time)
        if sort == 'asc':
            q = q.order_by(asc(ArchiveOrder.finish_time))
        else:
            q = q.order_by(desc(ArchiveOrder.finish_time))
        if page is not None and page_size is not None:
            q = q.offset((page - 1) * page_size).limit(page_size)
        return q.all()

    '''MchAccount'''
    # def add_mch_account(self, kwargs):
    #     return self.add_table('MchAccount', **kwargs)

    @models_to_list
    def get_mch_accounts(self, ktv_id=None, type=None, page=None, state=None, page_size=None):
        q = self.slave.query(MchAccount)
        if ktv_id is not None:
            q = q.filter(MchAccount.ktv_id == ktv_id)
        if type is not None:
            q = q.filter(MchAccount.type.in_(type))
        if state is not None:
            q = q.filter(MchAccount.state == state)
        if page is not None and page_size is not None:
            q = q.order_by(desc(MchAccount.id)).offset((page - 1) * page_size).limit(page_size)
        return q.all()

    @model_to_dict
    def get_mch_account(self, ktv_id=None, type=None, date=None):
        q = self.slave.query(MchAccount)
        if ktv_id is not None:
            q = q.filter(MchAccount.ktv_id == ktv_id)
        if type is not None:
            q = q.filter(MchAccount.type == type)
        if date is not None:
            q = q.filter(MchAccount.end_date == date)
        return q.scalar()

    @model_to_dict
    def get_mch_account_newest(self, ktv_id=None, type=None):
        q = self.master.query(MchAccount)
        if ktv_id is not None:
            q = q.filter(MchAccount.ktv_id == ktv_id)
        if type is not None:
            q = q.filter(MchAccount.type == type)
        q = q.order_by(desc(MchAccount.id)).limit(1)
        return q.scalar()

    def get_mch_account_count(self, ktv_id=None, type=None):
        q = self.slave.query(func.count('1'))
        if ktv_id is not None:
            q = q.filter(MchAccount.ktv_id == ktv_id)
        if type is not None:
            q = q.filter(MchAccount.type.in_(type))
        return q.scalar()

    def get_mch_account_sum(self, ktv_id=None, type=None):
        q = self.slave.query(func.sum(MchAccount.money))
        if ktv_id is not None:
            q = q.filter(MchAccount.ktv_id == ktv_id)
        if type is not None:
            q = q.filter(MchAccount.type == type)
        res = q.scalar()
        if not res:
            return 0
        return int(res)

    '''ZzhAccount'''

    @models_to_list
    def get_zzh_accounts(self, ktv_id=None, type=None, page=None, page_size=None):
        q = self.slave.query(ZzhAccount)
        if ktv_id is not None:
            q = q.filter(ZzhAccount.ktv_id == ktv_id)
        if type is not None:
            q = q.filter(ZzhAccount.type.in_(type))
        if page is not None and page_size is not None:
            q = q.order_by(desc(ZzhAccount.id)).offset((page - 1) * page_size).limit(page_size)
        return q.all()

    @model_to_dict
    def get_zzh_account(self, ktv_id=None, type=None, date=None):
        q = self.slave.query(ZzhAccount)
        if ktv_id is not None:
            q = q.filter(ZzhAccount.ktv_id == ktv_id)
        if type is not None:
            q = q.filter(ZzhAccount.type == type)
        if date is not None:
            q = q.filter(ZzhAccount.end_date == date)
        return q.scalar()

    @model_to_dict
    def get_zzh_account_newest(self, ktv_id=None, type=None):
        q = self.master.query(ZzhAccount)
        if ktv_id is not None:
            q = q.filter(ZzhAccount.ktv_id == ktv_id)
        if type is not None:
            q = q.filter(ZzhAccount.type == type)
        q = q.order_by(desc(ZzhAccount.id)).limit(1)
        return q.scalar()

    def get_zzh_account_count(self, ktv_id=None, type=None):
        q = self.slave.query(func.count('1'))
        if ktv_id is not None:
            q = q.filter(ZzhAccount.ktv_id == ktv_id)
        if type is not None:
            q = q.filter(ZzhAccount.type.in_(type))
        return q.scalar()

    def get_zzh_account_sum(self, ktv_id=None, type=None):
        q = self.slave.query(func.sum(ZzhAccount.money))
        if ktv_id is not None:
            q = q.filter(ZzhAccount.ktv_id == ktv_id)
        if type is not None:
            q = q.filter(ZzhAccount.type == type)
        res = q.scalar()
        if not res:
            return 0
        return int(res)

    '''MchFinancial'''
    @models_to_list
    def get_mch_profits(self, ktv_id=None, page=None, page_size=None):
        q = self.master.query(MchFinancial)
        if ktv_id is not None:
            q = q.filter(MchFinancial.ktv_id == ktv_id)
        if page is not None and page_size is not None:
            q = q.order_by(desc(MchFinancial.date)).offset((page - 1) * page_size).limit(page_size)
        return q.all()

    def get_mch_financial_sum_profit(self, ktv_id=None):
        q = self.slave.query(func.sum(MchFinancial.profit))
        if ktv_id is not None:
            q = q.filter(MchFinancial.ktv_id == ktv_id)
        res = q.scalar()
        if not res:
            return 0
        return int(res)

    '''MchIncome'''
    def update_mch_income(self, ktv_id=None, state=None, date=None, data=None):
        q = self.master.query(MchIncome)
        if ktv_id is not None:
            q = q.filter(MchIncome.ktv_id == ktv_id)
        if state is not None:
            q = q.filter(MchIncome.state == state)
        if date is not None:
            q = q.filter(MchIncome.date <= date)
        if data is not None:
            q.update(data)
        self.master.commit()

    @model_to_dict
    def get_mch_income(self, id):
        res = self.slave.query(MchIncome).filter(MchIncome.id == id).scalar()
        return res

    @model_to_dict
    def get_mch_income_newest(self, ktv_id=None):
        q = self.master.query(MchIncome)
        if ktv_id is not None:
            q = q.filter(MchIncome.ktv_id == ktv_id)
        q = q.order_by(desc(MchIncome.date)).limit(1)
        return q.scalar()

    @models_to_list
    def get_mch_incomes(self, ktv_id=None, start_date=None, end_date=None, page=None, page_size=None, state=None):
        q = self.slave.query(MchIncome).order_by(desc(MchIncome.date))
        if ktv_id is not None:
            q = q.filter(MchIncome.ktv_id == ktv_id)
        if start_date is not None:
            q = q.filter(MchIncome.date >= start_date)
        if end_date is not None:
            q = q.filter(MchIncome.date <= end_date)
        if state is not None:
            q = q.filter(MchIncome.state == state)
        if page is not None and page_size is not None:
            q = q.offset((page - 1) * page_size).limit(page_size)
        return q.all()

    def get_mch_income_count(self, ktv_id=None, start_date=None, end_date=None, state=None):
        q = self.slave.query(func.count('1'))
        if ktv_id is not None:
            q = q.filter(MchIncome.ktv_id == ktv_id)
        if start_date is not None:
            q = q.filter(MchIncome.date >= start_date)
        if end_date is not None:
            q = q.filter(MchIncome.date <= end_date)
        if state is not None:
            q = q.filter(MchIncome.state == state)
        return q.scalar()

    def get_mch_income_normal_sum(self, ktv_id=None, start_date=None, end_date=None, state=None):
        q = self.slave.query(func.sum(MchIncome.normal_fee).label('fee'),
                             func.sum(MchIncome.normal_rate).label('rate'),
                             func.min(MchIncome.start_time).label('start_time'),
                             func.max(MchIncome.end_time).label('end_time'),
                             func.min(MchIncome.pos_start_time).label('pos_start_time'),
                             func.max(MchIncome.pos_end_time).label('pos_end_time'))
        if ktv_id is not None:
            q = q.filter(MchIncome.ktv_id == ktv_id)
        if state is not None:
            q = q.filter(MchIncome.state == state)
        if start_date is not None:
            q = q.filter(MchIncome.date >= start_date)
        if end_date is not None:
            q = q.filter(MchIncome.date <= end_date)
        res = q.first()

        normal_fee = int(res.fee) if res.fee else 0
        normal_rate = int(res.rate) if res.rate else 0

        return {
            'total_fee': normal_fee,
            'total_rate': normal_rate,
            'start_time': res.start_time,
            'end_time': res.end_time,
            'pos_start_time': res.pos_start_time,
            'pos_end_time': res.pos_end_time,
        }

    def get_mch_income_zzh_sum(self, ktv_id=None, start_date=None, end_date=None, state=None):
        q = self.slave.query(func.sum(MchIncome.zzh_fee).label('fee'),
                             func.sum(MchIncome.zzh_rate).label('rate'),
                             func.min(MchIncome.start_time).label('start_time'),
                             func.max(MchIncome.end_time).label('end_time'),
                             func.min(MchIncome.pos_start_time).label('pos_start_time'),
                             func.max(MchIncome.pos_end_time).label('pos_end_time'))
        if ktv_id is not None:
            q = q.filter(MchIncome.ktv_id == ktv_id)
        if state is not None:
            q = q.filter(MchIncome.state == state)
        if start_date is not None:
            q = q.filter(MchIncome.date >= start_date)
        if end_date is not None:
            q = q.filter(MchIncome.date <= end_date)
        res = q.first()

        zzh_fee = int(res.fee) if res.fee else 0
        zzh_rate = int(res.rate) if res.rate else 0

        return {
            'total_fee': zzh_fee,
            'total_rate': zzh_rate,
            'start_time': res.start_time,
            'end_time': res.end_time,
            'pos_start_time': res.pos_start_time,
            'pos_end_time': res.pos_end_time,
        }

    '''KtvAccount'''
    def insert_ktv_account(self, values):
        self.master.add(KtvAccount(**values))
        self.master.commit()

    def get_ktv_account_count(self, ktv_id=None):
        q = self.slave.query(func.count('1'))
        if ktv_id is not None:
            q = q.filter(KtvAccount.ktv_id == ktv_id)
        return q.scalar()

    @models_to_list
    def get_ktv_accounts(self, ktv_id=None, page=None, page_size=None):
        q = self.slave.query(KtvAccount)
        if ktv_id:
            q = q.filter(KtvAccount.ktv_id == ktv_id)
        if page and page_size:
            q = q.order_by(desc(KtvAccount.finish_time)).offset((page - 1) * page_size).limit(page_size)
        return q.all()

    def get_ktv_account_sum(self, ktv_id):
        q = self.slave.query(func.sum(KtvAccount.withdraw_money)).filter(KtvAccount.ktv_id == ktv_id)
        res = q.scalar()
        if not res:
            res = 0
        return int(res)

    @model_to_dict
    def get_ktv_account_newest(self, ktv_id=None):
        return self.master.query(KtvAccount).filter(KtvAccount.ktv_id == ktv_id).order_by(desc(KtvAccount.create_time)).limit(1).first()

    def get_pos_cnt(self, ktv_id):
        return self.slave.query(func.count('1')).filter(Pos.ktv_id == ktv_id).scalar()

    def get_pos_ktv_id(self, term_id):
        return self.slave.query(Pos.ktv_id).filter(Pos.term_id == term_id).scalar()

    '''MarketOrder'''
    def get_market_order_count(self, ktv_id=None):
        q = self.slave.query(func.count('1'))
        if ktv_id is not None:
            q = q.filter(MarketOrder.ktv_id == ktv_id)
        return q.scalar()

    @models_to_list
    def get_market_orders(self, ktv_id=None, money=None, page=None, page_size=None):
        q = self.slave.query(MarketOrder)
        if ktv_id is not None:
            q = q.filter(MarketOrder.ktv_id == ktv_id)
        if money is not None:
            q = q.filter(MarketOrder.money == money)
        if page is not None and page_size is not None:
            q = q.order_by(desc(MarketOrder.id)).offset((page - 1) * page_size).limit(page_size)
        return q.all()

    '''MarketCartItem'''
    @models_to_list
    def get_market_cart(self, ktv_id=None):
        q = self.slave.query(MarketCartItem).filter(MarketCartItem.is_true == 1)
        if ktv_id is not None:
            q = q.filter(MarketCartItem.ktv_id == ktv_id)
        return q.all()

    @model_to_dict
    def get_market_cart_item(self, ktv_id, product_item_id):
        return self.slave.query(MarketCartItem).filter(MarketCartItem.ktv_id == ktv_id)\
            .filter(MarketCartItem.product_item_id == product_item_id).filter(MarketCartItem.is_true == 1).scalar()

    def update_market_cart_item(self, market_cart_id, data):
        self.master.query(MarketCartItem).filter_by(id=market_cart_id).update(data)
        self.master.commit()

    '''MarketAddress'''
    def update_market_address(self, address_id, data):
        self.master.query(MarketAddress).filter(MarketAddress.id == address_id).update(data)
        self.master.commit()

    def delete_market_address(self, address_id):
        self.master.query(MarketAddress).filter(MarketAddress.id == address_id).delete()
        self.master.commit()

    @models_to_list
    def get_market_address_list(self, ktv_id):
        return self.slave.query(MarketAddress).filter(MarketAddress.ktv_id == ktv_id).all()

    @model_to_dict
    def get_market_address(self, address_id):
        return self.slave.query(MarketAddress).filter(MarketAddress.id == address_id).scalar()

    '''MarketProduct'''
    @model_to_dict
    def get_market_product(self, product_id=None, is_tg=None):
        q = self.slave.query(MarketProduct)
        if product_id is not None:
            q = q.filter(MarketProduct.id == product_id)
        if is_tg is not None:
            q = q.filter(MarketProduct.is_tg == is_tg)
        return q.first()

    @models_to_list
    def get_market_products(self, product_id=None):
        q = self.slave.query(MarketProduct)
        if product_id is not None:
            q = q.filter(MarketProduct.id == product_id)
        return q.all()

    '''MarketProductItem'''
    def update_market_product_item(self, product_item_id, data):
        self.master.query(MarketProductItem).filter(MarketProductItem.id == product_item_id).update(data)
        self.master.commit()

    @models_to_list
    def get_market_product_items(self, product_id=None, ids=None):
        q = self.slave.query(MarketProductItem).filter(MarketProductItem.num)
        if product_id is not None:
            q = q.filter(MarketProductItem.product_id == product_id)
        if ids is not None:
            q = q.filter(MarketProductItem.id.in_(ids))
        return q.all()

    @model_to_dict
    def get_market_product_item(self, id):
        return self.slave.query(MarketProductItem).filter(MarketProductItem.id == id).scalar()

    def get_market_product_item_sum_buy_num(self, product_id):
        res = self.slave.query(func.sum(MarketProductItem.buy_num))\
            .filter(MarketProductItem.product_id == product_id).scalar()
        if not res:
            res = 0
        return int(res)


    @model_to_dict
    def get_ktv_agent(self, openid):
        return self.slave.query(KtvAgent).filter_by(openid=openid).scalar()

    @models_to_list
    def get_all_ktv_agents(self):
        return self.slave.query(KtvAgent).all()

    @model_to_dict
    def get_ktv_agent_with_phone_num(self, phone_num):
        return self.slave.query(KtvAgent).filter_by(phone_num=phone_num).filter_by(payed=1).scalar()

    @model_to_dict
    def get_ktv_agent_with_phone_num_whether_payed(self, phone_num):
        return self.slave.query(KtvAgent).filter_by(phone_num=phone_num).scalar()

    def update_ktv_agent(self, openid, data):
        self.master.query(KtvAgent).filter_by(openid=openid).update(data)
        self.master.commit()

    def update_ktv_agent_with_phone_num(self, phone_num, data):
        self.master.query(KtvAgent).filter_by(phone_num=phone_num).update(data)
        self.master.commit()

    @model_to_dict
    def add_ktv_agent(self, data={}):
        agent = KtvAgent(**data)
        self.master.add(agent)
        self.master.commit()
        return agent

    @model_to_dict
    def get_custom_ktv_by_kid(self, ktv_id, status=-1):
        q = self.slave.query(CustomKtv).filter_by(ktv_id=ktv_id)
        if status in (0, 1):
            q = q.filter_by(status=status)
        return q.scalar()

    @model_to_dict
    def get_custom_ktv_by_id(self, _id):
        return self.slave.query(CustomKtv).filter_by(id=_id).scalar()

    @models_to_list
    def get_custom_ktvs(self, openid):
        return self.slave.query(CustomKtv).filter_by(agent_openid=openid).all()

    @models_to_list
    def get_all_custom_ktvs(self):
        return self.slave.query(CustomKtv).all()

    def update_custom_ktv(self, _id, data):
        self.master.query(CustomKtv).filter_by(id=_id).update(data)
        self.master.commit()

    @model_to_dict
    def add_custom_ktv(self, data):
        ktv = CustomKtv(**data)
        self.master.add(ktv)
        self.master.commit()
        return ktv

    def delete_custom_ktv(self, _id):
        self.master.query(CustomKtv).filter_by(id=_id).delete()
        self.master.commit()

    @model_to_dict
    def add_custom_ktv_order(self, data):
        order = CustomKtvOrder(**data)
        self.master.add(order)
        self.master.commit()
        return order

    @models_to_list
    def get_project_orders(self, project_id):
        return self.slave.query(CustomKtvOrder).filter_by(custom_ktv_id=project_id).filter_by(state=2).order_by(CustomKtvOrder.update_time).all()

    def update_custom_ktv_order(self, order_id, data):
        self.master.query(CustomKtvOrder).filter_by(order_id=order_id).update(data)
        self.master.commit()

    @model_to_dict
    def get_custom_ktv_order(self, order_id):
        return self.slave.query(CustomKtvOrder).filter_by(order_id=order_id).scalar()

    @model_to_dict
    def get_gzh_user(self, openid, ktv_id):
        return self.slave.query(GzhUser).filter_by(openid=openid).filter_by(ktv_id=ktv_id).scalar()

    @models_to_list
    def get_ktv_agent_with_province_id(self, province_id):
        return self.slave.query(KtvAgent).filter_by(province_id=province_id).filter_by(payed=1).all()

    def update_gzh_user(self, openid, ktv_id, data):
        self.master.query(GzhUser).filter_by(openid=openid).filter_by(ktv_id=ktv_id).update(data)
        self.master.commit()

    @model_to_dict
    def add_gzh_user(self, **data):
        key = 'insert_gzh_user_%s_%s' % (data.get('openid'), data.get('ktv_id'))
        if not control.ctrl.rs.setnx(key, 1):
            return
        control.ctrl.rs.expire(key, 5)
        user = GzhUser(**data)
        self.master.add(user)
        self.master.commit()
        return user

    @models_to_list
    def get_gzh_orders(self, ktv_id, openid='', state=0, page=1, page_size=10, expired=-1, status=-1, tp='',
                       from_date='', to_date='', query='', fifteen=0, tps=None):
        q = self.slave.query(GzhOrder).filter_by(ktv_id=ktv_id)
        if state:
            q = q.filter_by(state=state)
        if openid:
            q = q.filter_by(openid=openid)
        if tp:
            q = q.filter_by(tp=tp)
        if expired in (0, 1):
            now = datetime.datetime.now().date()
            if expired:
                q = q.filter(func.date(GzhOrder.expire_time)<now)
            else:
                q = q.filter(func.date(GzhOrder.expire_time)>=now)
        if tp:
            q = q.filter_by(tp=tp)
        if tps:
            q = q.filter(GzhOrder.tp.in_(tps))
        if status in (0, 1):
            q = q.filter_by(status=status)
        if from_date and to_date:
            q = q.filter(func.date(GzhOrder.create_time)>=from_date).filter(func.date(GzhOrder.create_time)<=to_date)
        if query:
            q = q.filter(or_(GzhOrder.phone_num.like('%'+query+'%'), GzhOrder.order_id.like('%'+query+'%')))
        if fifteen:
            fifteen_min_ago = datetime.datetime.now() - datetime.timedelta(minutes=15)
            q = q.filter(or_(GzhOrder.state==2, and_(GzhOrder.state!=2, GzhOrder.create_time > fifteen_min_ago)))

        offset = (page - 1) * page_size
        return q.order_by(GzhOrder.update_time.desc()).offset(offset).limit(page_size).all()

    def get_gzh_orders_count(self, ktv_id, openid='', state=0, expired=-1, status=-1, tp='',
                             from_date='', to_date='', query='', fifteen=0, tps=None):
        q = self.slave.query(func.count('1')).select_from(GzhOrder).filter_by(ktv_id=ktv_id)
        if state:
            q = q.filter_by(state=state)
        if openid:
            q = q.filter_by(openid=openid)
        if tp:
            q = q.filter_by(tp=tp)
        if tps:
            q = q.filter(GzhOrder.tp.in_(tps))
        if expired in (0, 1):
            now = datetime.datetime.now().date()
            if expired:
                q = q.filter(func.date(GzhOrder.expire_time)<now)
            else:
                q = q.filter(func.date(GzhOrder.expire_time)>=now)
        if tp:
            q = q.filter_by(tp=tp)
        if status in (0, 1):
            q = q.filter_by(status=status)
        if from_date and to_date:
            q = q.filter(func.date(GzhOrder.create_time)>=from_date).filter(func.date(GzhOrder.create_time)<=to_date)
        if query:
            q = q.filter(or_(GzhOrder.phone_num.like('%'+query+'%'), GzhOrder.order_id.like('%'+query+'%')))
        if fifteen:
            fifteen_min_ago = datetime.datetime.now() - datetime.timedelta(minutes=15)
            q = q.filter(or_(GzhOrder.state!=1, (GzhOrder.state==1 and GzhOrder.create_time > fifteen_min_ago)))
        return q.scalar()

    @models_to_list
    def get_all_gzh_orders(self, ktv_id):
        return self.slave.query(GzhOrder).filter(GzhOrder.tp.in_(['groupon', 'buffet'])).filter_by(ktv_id=ktv_id, state=2).all()

    @model_to_dict
    def get_gzh_order(self, order_id):
        return self.slave.query(GzhOrder).filter_by(order_id=order_id).scalar()

    @model_to_dict
    def get_gzh_order_with_id(self, _id):
        return self.slave.query(GzhOrder).filter_by(id=_id).scalar()

    def update_gzh_order(self, order_id, data):
        self.master.query(GzhOrder).filter_by(order_id=order_id).update(data)
        self.master.commit()

    def update_gzh_order_with_id(self, _id, data):
        self.master.query(GzhOrder).filter_by(id=_id).update(data)
        self.master.commit()

    @models_to_list
    def get_gzh_orders_with_order_ids(self, order_ids):
        return self.slave.query(GzhOrder).filter(GzhRemark.order_id.in_(order_ids)).all()

    @model_to_dict
    def add_gzh_order(self, data):
        order = GzhOrder(**data)
        self.master.add(order)
        self.master.commit()
        return order

    def add_custom_ktvs_with_kids(self, kids):
        for kid in kids:
            ktv = CustomKtv(ktv_id=kid, status=1, state=2, agent_openid='fake_openid')
            self.master.add(ktv)
            self.master.commit()

    def add_custom_ktv_orders_with_kids(self, kids):
        for kid in kids:
            try:
                custom_ktv = self.get_custom_ktv_by_kid(kid)
                order = CustomKtvOrder(custom_ktv_id=custom_ktv['id'], years=1, fee=1,state=2)
                self.master.add(order)
                self.master.commit()
            except:
                pass

    @model_to_dict
    def add_ktv_remark(self, data):
        remark = GzhRemark(**data)
        self.master.add(remark)
        self.master.commit()
        return remark

    def update_ktv_remark(self, _id, data):
        self.master.query(GzhRemark).filter_by(id=_id).update(data)
        self.master.commit()

    def delete_ktv_remark(self, _id):
        self.master.query(GzhRemark).filter_by(id=_id).delete()
        self.master.commit()

    @models_to_list
    def get_ktv_remarks(self, ktv_id, status=-1, grade=None):
        q = self.slave.query(GzhRemark).filter_by(ktv_id=ktv_id)
        if status in (0, 1, 2):
            q = q.filter_by(status=status)
        if grade:
            q = q.filter(GzhRemark.grade.in_(grade))
        return q.all()

    @models_to_list
    def get_paged_ktv_remarks(self, ktv_id, status=-1, grade=None, page=1, page_size=10):
        q = self.slave.query(GzhRemark).filter_by(ktv_id=ktv_id)
        if status in (0, 1, 2):
            q = q.filter_by(status=status)
        if grade:
            q = q.filter(GzhRemark.grade.in_(grade))
        offset = (page - 1) * page_size
        return q.order_by(GzhRemark.update_time.desc()).offset(offset).limit(page_size).all()

    def get_ktv_remarks_count(self, ktv_id, status=-1, grade=None):
        q = self.slave.query(func.count('1')).select_from(GzhRemark).filter_by(ktv_id=ktv_id)
        if status in (0, 1, 2):
            q = q.filter_by(status=status)
        if grade:
            q = q.filter(GzhRemark.grade.in_(grade))
        return q.scalar()

    @models_to_list
    def get_earn_sum_rank(self):
        res = self.slave.query(GzhUser).order_by(GzhUser.earn_sum.desc()).limit(10).all()
        return res

    def update_dis_order(self, order_id, data):
        q = self.master.query(GzhDisOrder).filter_by(order_id=order_id)
        if q.scalar():
            print('aaaaaaaaaa')
            q.update(data)
        else:
            print('bbbbbbbbbb')
            self.master.add(GzhDisOrder(**data))
        self.master.commit()

    def update_card_order(self, order_id, data):
        q = self.master.query(CardOrder).filter_by(order_id=order_id)
        if q.scalar():
            q.update(data)
        else:
            self.master.add(CardOrder(**data))
        self.master.commit()

    @model_to_dict
    def get_dis_order(self, order_id):
        res = self.slave.query(GzhDisOrder).filter_by(order_id=order_id).scalar()
        return res

    def update_dis_user_earn_sum(self, open_id, ktv_id, add_fee):
        q = self.slave.query(GzhUser).filter_by(openid=open_id, ktv_id=ktv_id)
        user_info = q.scalar()
        user_info = model2dict(user_info)
        print(100 * '*')
        print(user_info)
        data = dict(earn_sum=user_info['earn_sum'] + add_fee)
        print(data)
        q.update(data)
        self.master.commit()

    @models_to_list
    def ktv_coupon_create_his(self):
        coupon_list = self.slave.query(CardOrder).filter_by(state=2).order_by(CardOrder.create_time.desc()).limit(10).all()
        return coupon_list

    @model_to_dict
    def add_gzh_buffet(self, data):
        buffet = GzhBuffet(**data)
        self.master.add(buffet)
        self.master.commit()
        return buffet

    def update_gzh_buffet(self, _id, data):
        self.master.query(GzhBuffet).filter_by(id=_id).update(data)
        self.master.commit()

    def update_gzh_buffet_kid_not_in_ids(self, ktv_id, _ids, data):
        '''主要用于批量下线'''
        self.master.query(GzhBuffet).filter_by(ktv_id=ktv_id).filter(~GzhBuffet.id.in_(_ids)).update(data)
        self.master.commit()

    @models_to_list
    def get_gzh_buffets(self, ktv_id, status=-1):
        q = self.slave.query(GzhBuffet).filter_by(ktv_id=ktv_id)
        if status in (0, 1):
            q = q.filter_by(status=status)
        return q.all()

    @model_to_dict
    def get_gzh_buffet(self, _id):
        return self.slave.query(GzhBuffet).filter_by(id=_id).scalar()

    @model_to_dict
    def add_gzh_groupon(self, data):
        groupon = GzhGroupon(**data)
        self.master.add(groupon)
        self.master.commit()
        return groupon

    def update_gzh_groupon(self, _id, data):
        self.master.query(GzhGroupon).filter_by(id=_id).update(data)
        self.master.commit()

    @models_to_list
    def get_gzh_groupons(self, ktv_id, status=-1, expired=-1):
        q = self.slave.query(GzhGroupon).filter_by(ktv_id=ktv_id)
        if status in (0, 1):
            q = q.filter_by(status=status)
        if expired in (0, 1):
            now = datetime.datetime.now().date()
            if expired:
                q = q.filter(func.date(GzhGroupon.expire)<now)
            else:
                q = q.filter(func.date(GzhGroupon.expire)>=now)
        return q.all()

    @model_to_dict
    def get_gzh_groupon(self, _id):
        return self.slave.query(GzhGroupon).filter_by(id=_id).scalar()

    def update_gzh_groupons_kid_not_in_ids(self, ktv_id, _ids=None, data={}):
        '''批量下线: 编辑时，所有的数据一次性传，用户有做修改，有做删除'''
        self.master.query(GzhGroupon).filter_by(ktv_id=ktv_id).filter(GzhGroupon.id.in_(_ids)).update(data)
        self.master.commit()

    def grounding_gzh_groupons(self, ids, status):
        self.master.query(GzhGroupon).filter(GzhGroupon.id.in_(ids)).update({'status': status}, synchronize_session=False)
        self.master.commit()

    def grounding_gzh_buffets(self, ids, status):
        self.master.query(GzhBuffet).filter(GzhBuffet.id.in_(ids)).update({'status': status}, synchronize_session=False)
        self.master.commit()

    @model_to_dict
    def get_ktv_wx(self, ktv_id):
        return self.slave.query(KtvWx).filter_by(ktv_id=ktv_id).scalar()

    @models_to_list
    def get_all_ktv_wxs(self):
        return self.slave.query(KtvWx).all()

    @model_to_dict
    def add_gzh_lottery(self, data={}):
        lottery = GzhLottery(**data)
        self.master.add(lottery)
        self.master.commit()
        return lottery

    @model_to_dict
    def add_gzh_lottery_activity(self, data={}):
        activity = GzhLotteryActivity(**data)
        self.master.add(activity)
        self.master.commit()
        return activity

    @model_to_dict
    def add_gzh_lottery_record(self, data={}):
        record = GzhLotteryRecord(**data)
        self.master.add(record)
        self.master.commit()
        return record

    @model_to_dict
    def get_gzh_lottery(self, pk):
        return self.slave.query(GzhLottery).filter_by(id=pk).scalar()

    @models_to_list
    def get_gzh_lotteries(self, ktv_id):
        return self.slave.query(GzhLottery).filter_by(ktv_id=ktv_id).all()

    def update_gzh_lottery(self, pk, data={}):
        self.master.query(GzhLottery).filter_by(id=pk).update(data)
        self.master.commit()

    @model_to_dict
    def get_gzh_lottery_record(self, code, ktv_id):
        return self.slave.query(GzhLotteryRecord).filter_by(ktv_id=ktv_id, code=code).scalar()

    def update_gzh_lottery_record(self, code, ktv_id, data={}):
        self.master.query(GzhLotteryRecord).filter_by(ktv_id=ktv_id, code=code).update(data)
        self.master.commit()

    @model_to_dict
    def get_gzh_lottery_activity(self, pk, ktv_id=0):
        q = self.slave.query(GzhLotteryActivity)
        if pk:
            return q.filter_by(id=pk).scalar()
        return q.filter_by(ktv_id=ktv_id).scalar()

    def update_gzh_lottery_activity(self, pk, data={}):
        self.master.query(GzhLotteryActivity).filter_by(id=pk).update(data)
        self.master.commit()

    def update_gzh_lottery_activity_with_kid(self, ktv_id, data={}):
        self.master.query(GzhLotteryActivity).filter_by(ktv_id=ktv_id).update(data)
        self.master.commit()

    def get_gzh_user_lottery_count_of_ktv(self, ktv_id, openid):
        return self.master.query(func.count('1')).select_from(GzhOrder).filter_by(ktv_id=ktv_id, openid=openid, state=2, lottery=0).scalar()

    @models_to_list
    def get_ktv_lottery_record(self, ktv_id, page=1):
        q = self.slave.query(GzhLotteryRecord).filter_by(ktv_id=ktv_id)
        if page:
            q = q.order_by(GzhLotteryRecord.create_time.desc()).limit(10)
        return q.all()

    def get_gzh_lottery_get_count(self, lottery_id):
        return self.slave.query(func.count('1')).select_from(GzhLotteryRecord).filter_by(lottery_id=lottery_id, status=1).scalar()

    @models_to_list
    def get_gzh_user_lottery_records_of_ktv(self, ktv_id, openid):
        return self.slave.query(GzhLotteryRecord).filter_by(ktv_id=ktv_id, openid=openid).all()

    @models_to_list
    def get_user_first_gzh_order(self, ktv_id, openid):
        return self.slave.query(GzhOrder).filter_by(ktv_id=ktv_id, openid=openid, lottery=0, state=2).order_by(GzhOrder.create_time.asc()).limit(1).all()

    @model_to_dict
    def search_lottery_record(self, ktv_id, code):
        return self.slave.query(GzhLotteryRecord).filter_by(ktv_id=ktv_id, status=0, code=code).scalar()

    @models_to_list
    def get_gzh_user_orders(self, ktv_id, openid):
        return self.slave.query(GzhOrder).filter_by(ktv_id=ktv_id, openid=openid, lottery=1).limit(1).all()

    @models_to_list
    def get_card_member(self, ktv_id, phone_num):
        return self.slave.query(CardMember).filter_by(ktv_id=ktv_id, phone_num=phone_num).all()

    @model_to_dict
    def add_gzh_user_coupon(self, data={}):
        coupon = GzhUserCoupon(**data)
        self.master.add(coupon)
        self.master.commit()
        return coupon

    @models_to_list
    def get_gzh_user_coupons(self, ktv_id, openid):
        '''
        当前只是将生日券入库（因为生日券可以多次领）
        以后可以全入库
        '''
        now = datetime.datetime.now().date()
        return self.slave.query(GzhUserCoupon).filter_by(ktv_id=ktv_id, openid=openid, status=0).filter(func.date(GzhUserCoupon.expire_time)>=now).all()


if __name__ == '__main__':
    Base.metadata.create_all(engine, checkfirst=True)

