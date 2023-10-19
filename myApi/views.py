from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import EmployeeSerializers
# Create your views here.
from phonepe.sdk.pg.payments.v1.payment_client import PhonePePaymentClient
from phonepe.sdk.pg.env import Env
from rest_framework.views import APIView
merchant_id = "GRAVITONWEBONLINE"  
salt_key = "398ea4c5-782b-4206-9d27-2e1a9aacb1b4"  
salt_index = 1 
env = Env.PROD # Change to Env.PROD when you go live

phonepe_client = PhonePePaymentClient(merchant_id=merchant_id, salt_key=salt_key, salt_index=salt_index, env=env)
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializers

import uuid  
from phonepe.sdk.pg.payments.v1.models.request.pg_pay_request import PgPayRequest

def initiate_phonepe_payment(request):
    unique_transaction_id = str(uuid.uuid4())
    s2s_callback_url = "https://www.merchant.com/callback"
    amount = 100
    id_assigned_to_user_by_merchant = 'YOUR_USER_ID'

    pay_page_request = PgPayRequest.pay_page_pay_request_builder(
        merchant_transaction_id=unique_transaction_id,
        amount=amount,
        merchant_user_id=id_assigned_to_user_by_merchant,
        callback_url=s2s_callback_url
    )

    try:
        pay_page_response = PHONEPE_CLIENT.pay(pay_page_request)
        pay_page_url = pay_page_response.data.instrument_response.redirect_info.url
        return JsonResponse({'pay_page_url': pay_page_url})
    except Exception as e:
        return JsonResponse({'error': str(e)})

from django.http import JsonResponse
class Initiate_phonepe_payment(APIView):
    def post(self, request, format=None):
        unique_transaction_id = str(uuid.uuid4())
        data =request.data
        s=Candidate.objects.create(Name=data["name"],Email=data["email"],PhoneNo=data["phoneNo"],amount=data["amount"],trnsId=data["trnsId"],userid=data["userid"])
        s.save()
        print(data)
        s2s_callback_url = "https://www.gravitonweb.com/webTalentGravity/Success"
        amount = 100
        id_assigned_to_user_by_merchant = "user-"+str(data["userid"])

        pay_page_request = PgPayRequest.pay_page_pay_request_builder(
            merchant_transaction_id=data["trnsId"],
            amount=data["amount"],
            merchant_user_id="user-"+str(data["userid"]),
            callback_url="https://www.gravitonweb.com/webTalentGravity/Success"
        )

        try:
            pay_page_response = phonepe_client.pay(pay_page_request)
            pay_page_url = pay_page_response.data.instrument_response.redirect_info.url
            return JsonResponse({'pay_page_url': pay_page_url})
        except Exception as e:
            return JsonResponse({'error': str(e)})