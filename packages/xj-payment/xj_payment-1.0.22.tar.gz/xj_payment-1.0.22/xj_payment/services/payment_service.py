import logging
import random
from datetime import datetime

import pytz
import requests
import time

from django.forms import model_to_dict
from django.utils import timezone

from xj_finance.services.finance_service import FinanceService
from xj_finance.services.finance_transact_service import FinanceTransactService
from xj_enroll.service.enroll_services import EnrollServices
from xj_thread.services.thread_item_service import ThreadItemService
from xj_user.services.user_service import UserService
from xj_payment.models import PaymentPayment
from xj_user.services.user_sso_serve_service import UserSsoServeService
from ..services.payment_wechat_service import PaymentWechatService


class PaymentService:
    # 支付总接口
    @staticmethod
    def pay(params):
        # print(params)
        data = params
        # data['total_fee'] = float(params['total_amount']) * 100  # 元转分
        payment_data = None
        out_trade_no = timezone.now().strftime('%Y%m%d%H%M%S') + ''.join(
            map(str, random.sample(range(0, 9), 4)))  # 随机生成订单号
        params['out_trade_no'] = out_trade_no
        if params['enroll_id']:
            enroll_data, err_txt = EnrollServices.enroll_detail(params['enroll_id'])  # 判断是否是报名订单
            if err_txt:
                return "报名记录不存在"
            data['enroll_id'] = enroll_data['id']
            data['user_id'] = enroll_data['user_id']
            data['total_fee'] = float(enroll_data['unpaid_amount']) * 100  # 元转分
        # 单点登录信息
        sso_data, err = UserSsoServeService.user_sso_to_user(data['user_id'])
        if err:
            return "单点登录记录不存在"
        sso_data = model_to_dict(sso_data)
        data['openid'] = sso_data['sso_unicode']
        tz = pytz.timezone('Asia/Shanghai')
        # 返回时间格式的字符串
        # now_time = timezone.now().astimezone(tz=tz)
        # now_time_str = now_time.strftime("%Y.%m.%d %H:%M:%S")
        # 返回datetime格式的时间
        now_time = timezone.now().astimezone(tz=tz).strftime("%Y-%m-%d %H:%M:%S")
        now = datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')
        payment_data = {
            "order_no": out_trade_no,
            "enroll_id": data['enroll_id'],
            "user_id": data['user_id'],
            "total_amount": int(data['total_fee']),
            "create_time": now,
        }
        data['platform'] = 'muzpay'
        data['currency'] = 'CNY'

        if params.get("total_amount", 0):
            data['total_fee'] = float(params.get("total_amount", 0)) * 100  # 元转分

        PaymentPayment.objects.create(**payment_data)
        # 支付方式检查
        if params['payment_method'] == "applets":  # 微信小程序支付

            payment = PaymentWechatService.payment_applets_pay(data)

        elif params['payment_method'] == "balance":  # 余额支付
            payment = PaymentWechatService.payment_balance_pay(data)

        return payment

    # 退款总接口
    @staticmethod
    def refund(params):
        data = params
        data['total_fee'] = float(params['total_amount']) * 100  # 元转分
        data['refund_fee'] = float(params['refund_amount']) * 100  # 元转分
        data['out_trade_no'] = timezone.now().strftime('%Y%m%d%H%M%S') + ''.join(
            map(str, random.sample(range(0, 9), 4)))
        payment = PaymentWechatService.payment_refund(data)
        return payment
