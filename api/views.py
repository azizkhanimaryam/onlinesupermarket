from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from api.models import Payment, Order
from cart.models import Cart
import requests
from django.conf import settings

class PaymentVerifyView(APIView):
    def get(self, request):
        authority = request.GET.get('Authority')
        status = request.GET.get('Status')

        payment = get_object_or_404(Payment, authority=authority)

        if status == 'OK':
            # Verify the payment with Zarinpal
            verify_url = 'https://api.zarinpal.com/pg/v4/payment/verify.json'
            headers = {'Content-Type': 'application/json'}
            data = {
                'merchant_id': settings.ZARINPAL_MERCHANT_ID,
                'authority': authority,
                'amount': int(payment.amount * 10),  # Amount in Toman
            }

            response = requests.post(verify_url, json=data, headers=headers)
            response_data = response.json()

            if response_data['data']['code'] == 100:
                # Payment was successful
                payment.is_paid = True
                payment.paid_at = timezone.now()
                payment.save()

                # Deactivate the cart or perform any other post-payment actions
                payment.cart.is_active = False
                payment.cart.save()

                # Return success response with RefID
                return Response({'message': 'Payment successful', 'ref_id': response_data['data']['ref_id']})
            else:
                # Payment verification failed
                return Response({'error': response_data['errors']}, status=400)
        else:
            # Payment was not successful
            return Response({'message': 'Payment was not successful'}, status=400)

