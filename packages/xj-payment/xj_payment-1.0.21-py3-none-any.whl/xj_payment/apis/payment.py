from django.http import JsonResponse
from rest_framework.views import APIView

from xj_payment.services.payment_service import PaymentService
from ..utils.model_handle import parse_data


class Payment(APIView):
    def pay(self):
        params = parse_data(self)
        payment = PaymentService.pay(params)
        return JsonResponse({
            'err': 0,
            'msg': 'OK',
            "data": payment
        })

    def refund(self):
        params = parse_data(self)
        payment = PaymentService.refund(params)
        return JsonResponse({
            'err': 0,
            'msg': 'OK',
            "data": payment
        })
