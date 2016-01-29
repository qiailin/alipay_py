#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
A simple python Wechat MicroPay API

Doc: https://pay.weixin.qq.com/wiki/doc/api/micropay.php?chapter=9_10&index=1
'''

__author__ = 'Anthony Fu'

import OpenSSL
import requests
import datetime, base64, json, random, logging
import alipay_config

__request_default = {'charset': 'utf-8', 'sign_type': 'RSA', 'version': '1.0'}
__pay_bizcontent_default = {'scene': 'bar_code', 'timeout_express': '10m', 'subject': 'Alipay_py'}

# Module init
logger = logging.getLogger('alipay')
logger.setLevel(logging.DEBUG)
logger.propagate = False
fh = logging.FileHandler('alipay.log',encoding = "UTF-8")
fh.setLevel(logging.INFO)
fh.setFormatter(logging.Formatter('----------%(asctime)s---------- \n%(message)s','%Y/%m/%d %H:%M:%S'))
logger.addHandler(fh)
# Load configs
__cert = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, open(alipay_config.configs['private_key_path']).read())
__request_default['app_id'] = alipay_config.configs['app_id']
__pay_bizcontent_default['subject'] = alipay_config.configs['default_subject']

def log(text):
    def decorator(func):
        def wrapper(*args, **kw):
            result = func(*args, **kw)
            logger.info(text + '\n' + str(result))
            return result
        return wrapper
    return decorator


@log('pay')
def pay(total_amount, auth_code, subject = None):
    out_trade_no = __gen_trade_no()
    d = {}
    d.update(__pay_bizcontent_default)
    d.update({
        'out_trade_no': str(out_trade_no),
        'total_amount': str(total_amount),
        'auth_code': str(auth_code)
    })
    if subject:
        d.update({'subject': subject})
    content = json.dumps(d)
    r = __post(__gen_request('alipay.trade.pay', biz_content = content))
    response = json.loads(r.text)
    return response['alipay_trade_pay_response']

@log('query')
def query(out_trade_no):
    content = json.dumps({
        'out_trade_no': str(out_trade_no)
    })
    r = __post(__gen_request('alipay.trade.query', biz_content = content))
    return json.loads(r.text)['alipay_trade_query_response']

@log('refund')
def refund(trade_no, refund_amount, refund_reason = None):
    d = {
        'trade_no': str(trade_no),
        'refund_amount': str(refund_amount)
    }
    if refund_reason:
        d.update({'refund_reason': str(refund_reason)})
    content = json.dumps(d)
    r = __post(__gen_request('alipay.trade.refund', biz_content = content))
    return json.loads(r.text)['alipay_trade_refund_response']

@log('cancel')
def cancel(out_trade_no):
    content = json.dumps({
        'out_trade_no': str(out_trade_no)
    })
    r = __post(__gen_request('alipay.trade.cancel', biz_content = content))
    return json.loads(r.text)['alipay_trade_cancel_response']

@log('refund_out')
def refund_out(out_trade_no, refund_amount, refund_reason = None):
    r = query(out_trade_no)
    return refund(r['trade_no'],refund_amount,refund_reason)



def __join_dict(dic):
    return '&'.join('{}={}'.format(k, v) for k, v in sorted(dic.items()))


def __gen_sign(dic):
    data = __join_dict(dic).encode('utf-8')
    signature = OpenSSL.crypto.sign(__cert, data, 'sha1')
    return base64.standard_b64encode(signature).decode()


def __gen_trade_no():
    return 'zfb' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '0' + str(random.randint(10, 99))


def __gen_request(method, **kw):
    kw.update(__request_default)
    kw.update({'method': method, 'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
    kw.update({'sign': __gen_sign(kw)})
    return kw


def __post(data):
    return requests.post('https://openapi.alipay.com/gateway.do', data = data)
