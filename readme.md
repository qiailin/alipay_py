# Alipay
A simple python Alipay barcode trade API

## Usage
```python
>>> import alipay
>>> alipay.pay('0.01','285866953553783713')
{
    'receipt_amount': '0.01',
    'invoice_amount': '0.01',
    'buyer_logon_id': '*****@gmail.com',
    'fund_bill_list': [{
        'fund_channel': 'ALIPAYACCOUNT',
        'amount': '0.01'
    }],
    'trade_no': '201601292100100*************',
    'gmt_payment': '2016-01-29 18:07:29',
    'code': '10000',
    'point_amount': '0.00',
    'buyer_pay_amount': '0.01',
    'buyer_user_id': '208***********65',
    'out_trade_no': 'zfb20160129*********',
    'msg': 'Success',
    'total_amount': '0.01',
    'open_id': '208**************************066'
}
>>> alipay.refund('201601292100100*************',0.01)
{
    'buyer_user_id': '208***********65',
    'out_trade_no': 'zfb20160129*********,
    'send_back_fee': '0.01',
    'trade_no': '201601292100100*************',
    'open_id': '208**************************066',
    'code': '10000',
    'gmt_refund_pay': '2016-01-29 18:09:13',
    'msg': 'Success',
    'refund_detail_item_list': [{
        'amount': '0.01',
        'fund_channel': 'ALIPAYACCOUNT'
    }],
    'buyer_logon_id': '******@gmail.com',
    'refund_fee': '0.01',
    'fund_change': 'Y'
}
```

## Requires
Python 3.x
#### Libs
- requests
- pyOpenSSL

## Configs
/alipay_config.py
```python
configs = {
    'app_id'            : '',
    'private_key_path'  : 'cert/alipay_private_key.pem',
    'default_subject'   : 'Goods'
}
```

## Doc
[支付宝开放平台](https://doc.open.alipay.com/doc2/detail.htm?spm=0.0.0.0.rjj2Sr&treeId=26&articleId=103253&docType=1)