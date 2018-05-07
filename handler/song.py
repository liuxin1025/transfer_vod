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


class IndexHandler(BaseHandler):

    async def get(self):
        is_login = self.get_secure_cookie('is_login')
        source = self._d()
        if not is_login:
            return self.render('pay/login.tpl', username='', password='', source=source)
        ktv = await ctrl.pay.get_ktv_ctl(int(is_login))
        bank_info_exist_flag = ktv['bank_account'] != '' and ktv['bank_name'] != '' and ktv['bank_branch'] != '' and \
                               ktv['bank_phone'] != '' and ktv['account_name'] != ''

        if not bank_info_exist_flag and not self.is_guest():
            self.redirect('/mch/addbank')
            return

        if source == 'mobile':
            return self.render('pay/index.html')
        if source == 'pc':
            return self.render('index.html')


class IndexPcHandler(BaseHandler):

    async def get(self, other):
        is_login = self.get_secure_cookie('is_login')
        if not is_login:
            return self.render('pay/login.tpl', username='', password='', source=self._d())

        ktv = await ctrl.pay.get_ktv_ctl(int(is_login))
        bank_info_exist_flag = ktv['bank_account'] != '' and ktv['bank_name'] != '' and ktv['bank_branch'] != '' and \
                               ktv['bank_phone'] != '' and ktv['account_name'] != ''

        if not bank_info_exist_flag:
            self.redirect('/mch/addbank')
            return

        return self.render('index.html')


class IncomeListHandler(BaseHandler):

    @api_check_login
    async def get(self):
        res = {}
        try:
            ktv_id = self.ktv_id
            date = self.get_argument('date', '2016-10')
        except:
            raise utils.APIError(errcode=10001)
        data = date.split('-')
        year = data[0]
        month = data[1]

        start_date = '%s-%s-01' % (year, month)
        monthRange = calendar.monthrange(int(year), int(month))[1]
        end_date = '%s-%s-%s' % (year, month, monthRange)
        res['list'] = []
        yesterday = when.yesterday()
        if int(year) == yesterday.year and int(month) == yesterday.month:# 昨日营收
            ktv = await ctrl.pay.get_ktv_ctl(ktv_id)
            y_time = ctrl.mch.get_yeterday_income_time_ctl(ktv)
            if y_time:
                y_sum_fee = ctrl.mch.get_yesterday_order_sum_fee_ctl(ktv_id=ktv_id, tp=ORDER_TP['normal'], start_time=y_time['start_time'], end_time=y_time['end_time'], pos_start_time=y_time['pos_start_time'], pos_end_time=y_time['pos_end_time'])
                y_income = {
                    'start_time': y_time['start_time'],
                    'end_time': y_time['end_time'],
                    'pos_start_time': y_time['pos_start_time'],
                    'pos_end_time': y_time['pos_end_time'],
                    'normal_fee': y_sum_fee['total_fee'],
                    'normal_rate': y_sum_fee['total_rate'],
                    'normal_money': y_sum_fee['total_fee'] - y_sum_fee['total_rate'],
                    'state': 0,
                    'income_id': -1
                }
                res['list'].append(y_income)
        res['list'] += ctrl.mch.get_normal_incomes_ctl(ktv_id=ktv_id, start_date=start_date, end_date=end_date)
        res['date'] = date
        self.send_json(res)

class ExOrderHandler(BaseHandler):

    async def get(self, timestamp, sign):
        if not utils.check_sign_ex(timestamp, sign):
            raise utils.APIError(errcode=10001, errmsg='验签错误')
        is_guest = '1' if timestamp == '1111' else '0'
        self.set_secure_cookie('is_guest', is_guest)

        order_id = self.get_argument('order_id', None)

        if not order_id:
            raise utils.APIError(errcode=10001, errmsg='订单号不得为空')
        res = ctrl.mch.get_order_ex_ctl(order_id)
        self.send_json(res)

class ExOrderListHandler(BaseHandler):

    async def get(self, timestamp, sign):
        if not utils.check_sign_ex(timestamp, sign):
            raise utils.APIError(errcode=10001, errmsg='验签错误')
        is_guest = '1' if timestamp == '1111' else '0'
        self.set_secure_cookie('is_guest', is_guest)

        term_id = self.get_argument('term_id', None)
        start_time = self.get_argument('start_time', '2017-04-11 00:00:00')
        end_time = self.get_argument('end_time', '2017-04-11 23:59:59')
        page = int(self.get_argument('page', '1'))
        page_size = int(self.get_argument('page_size', '20'))

        if not term_id:
            raise utils.APIError(errcode=10001, errmsg='终端号不得为空')
        if page_size > 100:
            raise utils.APIError(errcode=10001, errmsg='page_size > 100')

        res = {}
        res['list'] = ctrl.mch.get_orders_ex_ctl(term_id=term_id, start_time=start_time, end_time=end_time, page=page, page_size=page_size)
        self.send_json(res)

class OrderListHandler(BaseHandler):

    @api_check_login
    async def get(self):
        res={}
        try:
            ktv_id = self.ktv_id
            type = self.get_argument('type', '')
            channel = self.get_argument('channel', 'all')
            tp = self.get_argument('tp', 'normal')
            page = int(self.get_argument('page', '1'))
            start_time = self.get_argument('start_time', '')
            end_time = self.get_argument('end_time', '')
            sort = self.get_argument('sort', 'desc')
        except:
            raise utils.APIError(errcode=10001)
        channel = None if channel == 'all' else ORDER_CHANNEL[channel]
        tp = None if tp == 'all' else ORDER_TP[tp]
        if not type:# 查询 + 今日营收

            if not start_time and not end_time:# 今日营收
                ktv = await ctrl.pay.get_ktv_ctl(ktv_id)
                t_time = ctrl.mch.get_today_income_time_ctl(ktv)
                res['ktv_name'] = ktv['name']
                if page == 1:
                    t_sum_fee = ctrl.mch.get_today_order_sum_fee_ctl(ktv_id=ktv_id, tp=ORDER_TP['normal'], channel=channel, start_time=t_time['start_time'], end_time=t_time['end_time'], pos_start_time=t_time['pos_start_time'], pos_end_time=t_time['pos_end_time'])
                    t_sum_count = ctrl.mch.get_today_order_sum_count_ctl(ktv_id=ktv_id, tp=ORDER_TP['normal'], channel=channel, start_time=t_time['start_time'], end_time=t_time['end_time'], pos_start_time=t_time['pos_start_time'], pos_end_time=t_time['pos_end_time'])
                    res.update(
                        {
                            'start_time': t_time['start_time'],
                            'end_time': t_time['end_time'],
                            'pos_start_time': t_time['pos_start_time'],
                            'pos_end_time': t_time['pos_end_time'],
                            'total_fee': t_sum_fee['total_fee'],
                            'rate_fee': t_sum_fee['total_rate'],
                            'total_count': t_sum_count,
                            'state': self.get_argument('state', ''),
                        })
                res['list'] = ctrl.mch.get_m_orders_ctl(ktv_id=ktv_id, channel=channel, tp=tp, sort=sort, page=page, page_size=10, income_id=-2)
            else:# 查询
                if page == 1:
                    res['total_fee'], res['rate_fee'], res['total_count'] = ctrl.mch.get_order_sum_ctl(ktv_id=ktv_id, channel=channel, tp=tp, start_time=start_time, end_time=end_time)
                    res['state'] = self.get_argument('state','')
                res['list'] = ctrl.mch.get_orders_ctl(ktv_id=ktv_id, channel=channel, tp=tp, start_time=start_time, end_time=end_time, sort=sort, page=page, page_size=10)
                res['start_time'] = start_time
                res['end_time'] = end_time
                res['pos_start_time'] = start_time
                res['pos_end_time'] = end_time

        else:# 历史营收 income_id
            income_id = int(self.get_argument('income_id', '0'))
            if income_id == -1:# 昨日营收
                if page == 1:
                    ktv = await ctrl.pay.get_ktv_ctl(ktv_id)
                    y_time = ctrl.mch.get_yeterday_income_time_ctl(ktv)
                    res['total_fee'], res['rate_fee'], res['total_count'] = ctrl.mch.get_order_sum_ctl(ktv_id=ktv_id, channel=channel, tp=tp, income_id=income_id)
                    res['state'] = self.get_argument('state', '')
                    res.update({'start_time': y_time['start_time'], 'end_time': y_time['end_time'], 'pos_start_time': y_time['pos_start_time'], 'pos_end_time': y_time['pos_end_time']})
                res['list'] = ctrl.mch.get_orders_ctl(ktv_id=ktv_id, channel=channel, tp=tp, sort=sort, page=page, page_size=10, income_id=income_id)
            else:
                income = ctrl.mch.get_normal_income_ctl(income_id)
                if page == 1:
                    res['total_fee'], res['rate_fee'], res['total_count'] = ctrl.mch.get_order_sum_ctl(ktv_id=ktv_id, channel=channel, tp=tp, income_id=income_id)
                    res['state'] = self.get_argument('state','')
                    res.update({'start_time': income['start_time'], 'end_time': income['end_time'], 'pos_start_time': income['pos_start_time'], 'pos_end_time': income['pos_end_time']})
                res['list'] = ctrl.mch.get_orders_ctl(ktv_id=ktv_id, channel=channel, tp=tp, sort=sort, page=page, page_size=10, income_id=income_id)

        self.send_json(res)


class BillListHandler(BaseHandler):

    @api_check_login
    def get(self):
        res = {}
        try:
            ktv_id = self.ktv_id
            page = int(self.get_argument('page', '1'))
            type = self.get_argument('type', 'all')
        except:
            raise utils.APIError(errcode=10001)
        type = None if type == 'all' else BILL_TP[type]
        if page == 1:
            res['total_count'] = ctrl.mch.get_mch_account_count(ktv_id=ktv_id, type=type)
        mch_accounts = ctrl.mch.get_mch_accounts_ctl(ktv_id=ktv_id, type=type, page=page, page_size=10)
        res['list'] = mch_accounts
        res['date'] = mch_accounts[0]['create_time'].date() if mch_accounts else ''
        self.send_json(res)


class FinancialHandler(BaseHandler):

    @guest_not_allow
    @api_check_login
    async def post(self):
        try:
            ktv_id = self.ktv_id
            enable = int(self.get_argument('enable', 0))
        except:
            raise utils.APIError(errcode=10001, errmsg='参数错误')

        await ctrl.erp.update_ktv_ctl(ktv_id, {
            'is_financial': enable
        })
        self.send_json()


class SettleFastHandler(BaseHandler):

    @guest_not_allow
    @api_check_login
    async def post(self):
        ktv_id = self.ktv_id
        # 过滤多次点击
        key = 'fast_settle_%s' % ktv_id
        if not ctrl.rs.setnx(key, 1):
            raise utils.APIError(errcode=400, errmsg='请勿频繁点击，一分钟后再试，谢谢')
        ctrl.rs.expire(key, 60)
        ktv = await ctrl.pay.get_ktv_ctl(ktv_id)
        end_date = ctrl.mch.get_check_date_ctl()
        res = ctrl.mch.add_income_to_mch_account_ctl(ktv, end_date, is_fast=True)
        if res < 0:
            if res == -1:
                raise utils.APIError(errcode=1001, errmsg='请稍后再试')
            elif res == -2:
                raise utils.APIError(errcode=1001, errmsg='已结算过')
        ctrl.mch.update_mch_income(ktv_id=ktv_id, date=end_date, data={'state': 2})

        self.send_json()

    @api_check_login
    def get(self):
        ktv_id = self.ktv_id
        fast = ctrl.mch.get_fast_settlement_ctl(ktv_id)
        res = {
            'fee': fast['money'],
            'fast_rate': fast['fast_rate'],
            'date': fast['end_date']
        }
        res['money'] = res['fee'] - res['fast_rate']
        self.send_json(res)


class WithdrawHandler(BaseHandler):

    async def _get_ktv_bank_info(self, ktv, is_extra, bank_phone):
        if not ktv['bank_account']:
            raise utils.APIError(errcode=1001, errmsg='没有账号信息')
        if not is_extra and bank_phone and not ktv['bank_phone']:
            await ctrl.erp.update_ktv_ctl(ktv['store_id'], {
                'bank_phone': bank_phone
            })
        bank_info = ctrl.mch.get_bank_info_ctl(ktv, is_extra)
        return bank_info

    @guest_not_allow
    @api_check_login
    async def post(self):
        ktv_id = self.ktv_id
        # 过滤多次点击提现
        key = 'withdraw_%s' % ktv_id
        if not ctrl.rs.setnx(key, 1):
            raise utils.APIError(errcode=1001, errmsg='请勿频繁点击提现，一分钟后再试，谢谢')
        ctrl.rs.expire(key, 60)
        try:
            is_extra = int(self.get_argument('is_extra', 0))
            bank_phone = self.get_argument('bank_phone', '')
            withdraw_money = float(self.get_argument('money', 0))
        except:
            raise utils.APIError(errcode=10001, errmsy='参数错误')
        # 提现金额大于500
        if withdraw_money < 50000:
            raise utils.APIError(errcode=1001, errmsg='金额不足500')
        ktv = await ctrl.pay.get_ktv_ctl(ktv_id)
        if ktv['ktype'] == 6:   # 微官网代理商
            raise utils.APIError(errcode=1001, errmsg='请先联系钱阿银')

        bank_info = await self._get_ktv_bank_info(ktv, is_extra, bank_phone)
        res = ctrl.mch.add_withdraw_to_mch_account_ctl(ktv, withdraw_money, bank_info)
        if res < 0:
            if res == -1:
                raise utils.APIError(errcode=1001, errmsg='请稍后再试')
            elif res == -2:
                raise utils.APIError(errcode=1001, errmsg='您有一笔提现正在处理，请耐心等待~')
            elif res == -3:
                raise utils.APIError(errcode=1001, errmsg='提现金额不得大于账户余额')
        self.send_json()


class AccountHandler(BaseHandler):

    @api_check_login
    async def get(self):
        ktv_id = self.ktv_id
        ktv = await ctrl.pay.get_ktv_ctl(ktv_id)
        if not ktv:
            raise utils.APIError(errcode=10001)
        res = ctrl.mch.get_account_info_ctl(ktv)
        res['product'] = ctrl.market.get_tg_product_ctl()
        self.send_json(res)


class KtvNameHandler(BaseHandler):

    @api_check_login
    async def get(self):
        ktv_id = self.ktv_id
        ktv = await ctrl.pay.get_ktv_ctl(ktv_id)
        if not ktv:
            raise utils.APIError(errcode=10001)
        res = {
            'ktv_name': ktv['name']
        }
        self.send_json(res)


class ExportHandler(BaseHandler):

    def _money_format(self, fee):
        return '%.02f' % (fee / 100)

    def _tp_format(self, order):
        if int(order['tp']) != 0:
            return ['-', '电影', '美女红包', ''][int(order['tp'])]
        if 'baoyang' in order['other']:
            return '美女红包'
        if 'movie' in order['other']:
            return '电影'
        return '-'

    async def export(self, ktv_id):
        try:
            channel = self.get_argument('channel', 'all')
            tp = self.get_argument('tp', 'normal')
            type = self.get_argument('type', '')
            start_time = self.get_argument('start_time', '')
            end_time = self.get_argument('end_time', '')
            income_id = self.get_argument('income_id', '0')

        except Exception as e:
            logging.error(e)
            raise utils.APIError(errcode=10001)
        channel = None if channel == 'all' else ORDER_CHANNEL[channel]
        tp = None if tp == 'all' else ORDER_TP[tp]
        income_id = int(income_id) if income_id else 0
        data = []
        if not type: # time
            if not start_time and not end_time:# 今日营收
                ktv = await ctrl.pay.get_ktv_ctl(ktv_id)
                t_time = ctrl.mch.get_today_income_time_ctl(ktv)
                start_time = t_time['start_time']
                end_time = t_time['end_time']
            orders = ctrl.mch.get_orders_ctl(ktv_id=ktv_id, channel=channel, tp=tp, start_time=start_time, end_time=end_time)
        else: # income
            if income_id == -1:# 昨日营收
                orders = ctrl.mch.get_orders_ctl(ktv_id=ktv_id, channel=channel, tp=tp, income_id=income_id)
            else:
                orders = ctrl.mch.get_orders_ctl(ktv_id=ktv_id, channel=channel, tp=tp, income_id=income_id)
        if not orders:
            raise utils.APIError(errcode=1001, errmsg='无数据')

        if channel == ORDER_CHANNEL['wx']:
            name = '微信'
        elif channel == ORDER_CHANNEL['ali']:
            name = '支付宝'
        elif channel == ORDER_CHANNEL['pos']:
            name = 'pos'
        else:
            name = '全部'

        sheet_dict = {
            'sheetname': '%s进出账流水' % name,
            'titles': ['商户订单号', '订单费用(元)', '手续费用(元)', '订单创建时间', '支付类型', '卡号', '终端号']
        }
        for order in orders:
            sheet_dict.setdefault('data', []).append([order['order_id'], self._money_format(order['fee']),
                                                      self._money_format(order['rate']), order['finish_time'],
                                                      order['channel'], order['card_no'], order['term_id']])

        data.append(sheet_dict)
        if start_time and end_time:
            filename = 'static/data/进出账流水_%s~%s.xlsx' % (start_time, end_time)
        else:
            filename = 'static/data/进出账流水_%s.xlsx' % (str(income_id))
        filename_with_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), filename)
        utils.export_xlsx(data=data, export_filename=filename_with_path)
        self.set_header('Access-Control-Allow-Origin', '*')
        self.send_json(data={'url': '/' + filename})

    @api_check_login
    async def post(self):
        ktv_id = self.ktv_id
        await self.export(ktv_id)


class KtvHandler(BaseHandler):

    async def get(self, timestamp, ktv_id, sign):
        if not utils.check_sign(timestamp, ktv_id, sign):
            return self.render('error.tpl')
        self.set_secure_cookie('is_login', ktv_id, expires_days=1)
        is_guest = '1' if timestamp == '1111' else '0'
        self.set_secure_cookie('is_guest', is_guest)
        self.redirect('/mch')


class NotifyHandler(BaseHandler):

    @api_check_login
    def get(self):
        res = {
            'contents': ctrl.mch.get_mch_notify_ctl()
        }
        self.send_json(res)


class AddBankInfoHandler(BaseHandler):

    async def get(self):
        try:
            is_extra = int(self.get_argument('is_extra', 0))
        except:
            raise utils.APIError(errcode=10001)

        is_login = self.get_secure_cookie('is_login')
        ktv = await ctrl.pay.get_ktv_ctl(int(is_login))
        bank_info = ctrl.mch.get_account_info_ctl(ktv)
        return self.render('bank_new.tpl',
                           top_cate='withdraw',
                           action='deposit',
                           is_extra=is_extra,
                           bank_info=bank_info)


class WowAddBankInfoHandler(BaseHandler):

    @api_check_login
    async def get(self):
        try:
            is_extra = int(self.get_argument('is_extra', 0))
        except:
            raise utils.APIError(errcode=10001)

        ktv = await ctrl.pay.get_ktv_ctl(self.ktv_id)
        bank_info = ctrl.mch.get_account_info_ctl(ktv)
        return self.render('wow_add_bank.tpl',
                           top_cate='withdraw',
                           action='deposit',
                           is_extra=is_extra,
                           bank_info=bank_info)
