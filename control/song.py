#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
from datetime import datetime, timedelta
import when
from lib import utils
from settings import MCH_ACCOUNT_TYPE, FAST_RATE, UPYUN
from urllib.parse import urlencode
from tornado.httputil import url_concat

class SongCtrl(object):

    def __init__(self, ctrl):
        self.ctrl = ctrl
        self.api = ctrl.pdb.api

    def __getattr__(self, name):
        return getattr(self.api, name)

    def lock(self, key, lock_time=10):
        key = 'lock_%s' % key
        pl = self.ctrl.rs.pipeline(transaction=False)
        state, _ = pl.setnx(key, 1).expire(key, lock_time).execute()
        return state

    def unlock(self, key):
        key = 'lock_%s' % key
        self.ctrl.rs.delete(key)

    def get_tg_product(self):
        res = {}
        product = self.api.get_market_product(is_tg=1)
        if product:
            res = {
                'id': product['id'],
                'img': UPYUN['url'] + product['tg_img']
            }
        return res

    def get_products(self):
        res = []
        products = self.api.get_market_products()
        for product in products:
            item = {
                'id': product['id'],
                'name': product['name'],
                'img': UPYUN['url'] + product['main_img'],
                'price': product['price']
            }
            res.append(item)
        return res

    def get_product(self, ktv_id, product_id):
        product = self.api.get_market_product(product_id=product_id)
        if not product:
            return None
        product['details_img'] = UPYUN['url'] + product['details_img']
        product_items = self.api.get_market_product_items(product_id)
        for item in product_items:
            imgs = json.loads(item['imgs'])
            for img in imgs:
                img['min'] = UPYUN['url'] + img['min']
                img['max'] = UPYUN['url'] + img['max']
            item['imgs'] = imgs
        buy_num = self.api.get_market_product_item_sum_buy_num(product_id)
        res = {
            'name': product['name'],
            'price': product['price'],
            'freight': product['freight'],
            'params': json.loads(product['params']),
            'buy_num': buy_num,
            'details_img': product['details_img'],
            'items': product_items,
            'remark': product['remark'],
            'is_try': product['is_try'],
            'is_buy': 1,
        }
        if product['is_try']:
            res['is_try'] = 0 if self.api.get_market_orders(ktv_id=ktv_id, money=0) else 1
        if product['buy_object'] == 2:
            res['is_buy'] = 1 if self.api.get_pos_cnt(ktv_id) else 0
        res['not_buy_remark'] = '' if res['is_buy'] else product['not_buy_remark']

        return res

    def get_product_item(self, product_item_id):
        product_item = self.api.get_market_product_item(product_item_id)
        if not product_item:
            return {}
        res = {
            'id': product_item['id'],
            'name': product_item['name'],
            'price': product_item['price'],
            'spec': product_item['spec'],
            'img': json.loads(product_item['img'])[0],
        }
        return res

    def get_buy_product_items(self, items, is_try):
        res = {
            'total_money': 0,
            'freight': 0,
            'buy_items': []
        }
        product_total_money = 0
        item_dic = {}
        for item in items:
            item_dic[int(item['id'])] = int(item['num'])
        product_items = self.api.get_market_product_items(ids=list(item_dic.keys()))
        for product_item in product_items:
            buy_num = item_dic[product_item['id']]
            if not is_try and product_item['min_num'] and buy_num < product_item['min_num']:
                return -3
            if not is_try and product_item['max_num'] and buy_num > product_item['max_num']:
                return -4
            if buy_num > product_item['num']:
                return -2
            money = buy_num * product_item['price']
            data = {
                'id': product_item['id'],
                'name': product_item['name'],
                'price': product_item['price'],
                'spec': product_item['spec'],
                'img': UPYUN['url'] + json.loads(product_item['imgs'])[0]['min'] if product_item['imgs'] else '',
                'num': buy_num,
                'money': money
            }
            product_total_money += money
            res['buy_items'].append(data)
        if is_try:
            res['total_money'] = 0
        else:
            if product_total_money < 40000:
                res['freight'] = product_items[0]['freight']
            res['total_money'] = product_total_money + res['freight']
        return res

    def check_update_product_items(self, buy_items, is_try):
        res = {
            'product_total_money': 0,
            'freight': 0,
            'buy_items': []
        }
        product_item = {}
        for buy_item in buy_items:
            key = 'market_product_item_%s' % buy_item['id']
            state = self.lock_ctl(key, lock_time=10)
            if not state:
                return -1
            product_item = self.api.get_market_product_item(buy_item['id'])
            if not is_try and product_item['min_num'] and buy_item['num'] < product_item['min_num']:
                return -3
            if not is_try and product_item['max_num'] and buy_item['num'] > product_item['max_num']:
                return -4
            num = product_item['num'] - buy_item['num']
            buy_num = product_item['buy_num'] + buy_item['num']
            if num < 0:
                self.unlock_ctl(key)
                return -2
            self.unlock_ctl(key)
            self.api.update_market_product_item(buy_item['id'], {'num': num, 'buy_num': buy_num})

            money = buy_item['num'] * product_item['price']
            data = {
                'id': product_item['id'],
                'name': product_item['name'],
                'price': product_item['price'],
                'spec': product_item['spec'],
                'img': json.loads(product_item['imgs'])[0]['min'] if product_item['imgs'] else '',
                'num': buy_item['num'],
                'money': money
            }
            res['product_total_money'] += data['money']
            res['buy_items'].append(data)
        if is_try:
            res['product_total_money'] = 0
        else:
            if res['product_total_money'] < 40000:
                res['freight'] = product_item['freight']
        res['total_money'] = res['product_total_money'] + res['freight']
        return res

    def get_address_list(self, ktv_id):
        return self.api.get_market_address_list(ktv_id)

    def get_address(self, address_id):
        return self.api.get_market_address(address_id)

    def add_order(self, ktv_id=None, buy_items=None, address_id=None, product_total_money=None, freight=None):
        addr = self.api.get_market_address(address_id)
        addr.pop('create_time')
        addr.pop('update_time')
        data = {
            'ktv_id': ktv_id,
            'money': product_total_money + freight,
            'freight': freight,
            'buy_items': json.dumps(buy_items),
            'address': json.dumps(addr),
            'state': 1,
        }
        return self.api.add_table('MarketOrder', **data)

    def get_orders(self, ktv_id, page=None, page_size=None):
        orders_n = []
        orders = self.api.get_market_orders(ktv_id, page=page, page_size=page_size)
        for order in orders:
            buy_items = json.loads(order['buy_items'])
            for buy_item in buy_items:
                buy_item['img'] = UPYUN['url'] + buy_item['img']
            data = {
                'id': order['id'],
                'logistics': order['logistics'],
                'freight': order['freight'],
                'address': json.loads(order['address']),
                'buy_items': buy_items,
                'state': order['state'],
                'total_money': order['money']
            }
            orders_n.append(data)
        return orders_n

    def get_account_balance(self, ktv_id):
        account_newest = self.api.get_mch_account_newest(ktv_id=ktv_id)
        balance = account_newest['balance'] if account_newest else 0
        return balance

    def add_market_to_mch_account(self, ktv_id, money, order_id):
        state = self.lock_ctl('mch_account_%s' % ktv_id, lock_time=10)
        if not state:
            return -1
        account_newest = self.api.get_mch_account_newest(ktv_id=ktv_id)
        balance = account_newest['balance'] if account_newest else 0
        if money > balance:
            return -3
        balance -= money
        if balance < 0:
            return -4
        income_newest = self.api.get_mch_account_newest(ktv_id=ktv_id, type=MCH_ACCOUNT_TYPE['income'])
        data = {
            'ktv_id': ktv_id,
            'money': money,
            'balance': balance,
            'type': MCH_ACCOUNT_TYPE['market'],
            'state': 1,
            'detail': order_id,
            'end_date': income_newest['end_date'],
        }
        self.api.add_table('MchAccount', **data)
        return True

    def add_cart(self, ktv_id, product_item_id, num):
        cart_item = self.api.get_market_cart_item(ktv_id, product_item_id)
        if cart_item:
            new_num = cart_item['num'] + num
            self.api.update_marktet_cart_item(cart_item['id'], {'num': new_num})
        else:
            data = {
                'ktv_id': ktv_id,
                'product_item_id': product_item_id,
                'num': num
            }
            self.api.add_table('MarketCartItem', **data)

    # def get_products(self):
    #     products = self.api.get_market_products()
    #     for item in products:


