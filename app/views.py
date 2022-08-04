import base64
import json
from django.urls import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
import requests
from rest_framework.views import APIView
from rest_framework.response import Response


client_id = "ATL3_P1NOnX_ZN8GRtRubQRICv4PqKd7cG-UjlPSL6r26i7hLbfVXhwbgUdeUVYkQZeDi4Wle0NhEUYH"
secret_id = "EKFTshyysVUijehginE2iPbzsBTgnR46w4PGNrSNtptdkgO557mE3UHdyenCo696LM4RYQBKmR8nLjtv"


def view_that_asks_for_money(request):

    # What you want the button to do.
    paypal_dict = {
        "business": "receiver_email@example.com",
        "amount": "2000.00",
        "item_name": "name of the item",
        "invoice": "unique-invoice-id",
        "notify_url": request.build_absolute_uri(reverse('response')),
        "return": request.build_absolute_uri(reverse('response')),
        "cancel_return": request.build_absolute_uri(reverse('response')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "app/payment.html", context)

def res(request):
    
    return render(request, "app/response.html")

# from paypal.standard.forms import PayPalPaymentsForm

# class CustomPayPalPaymentsForm(PayPalPaymentsForm):
#     def get(self):
#         print("this is ok")
#         return """<button type="submit">Continue on PayPal get website</button>"""
#     # def get_html_submit_element(self):
#     #     return """<button type="submit">Continue on PayPal website</button>"""



class Get_token_for_payment(APIView):
    def get(self, request):
        url = "https://api.sandbox.paypal.com/v1/oauth2/token"
        data = {
            "client_id": client_id,
            "client_secret": secret_id,
            "grant_type": "client_credentials"
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic {0}".format(base64.b64encode((client_id + ":" + secret_id).encode()).decode())
        }

        token = requests.post(url, data, headers=headers)
        token = token.json()
        print(token)
        return Response({"access_token":token})


class Payment(APIView):
    def post(self, request):
        token = request.data["token"]
        print(token)
        headers = {"Content-Type": "application/json", "Authorization": 'Bearer ' +str(token)}
        url = "https://api.sandbox.paypal.com/v2/checkout/orders"
        data = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                "amount": {
                    "currency_code": "USD",
                    "value": "100.00"
                }
                }
            ]
        }
        data = json.dumps(data)
        result = requests.post(url, data, headers=headers)
        result = result.json()
        return Response({"result": result})