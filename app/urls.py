from django.urls import path, include
from app.views import view_that_asks_for_money , res, Get_token_for_payment, Payment

urlpatterns = [
    path('paypal/', view_that_asks_for_money),  
    path('response/', res, name = "response"),  
    path('get_token/', Get_token_for_payment.as_view(), name = "get_token"),  
    path('payment/', Payment.as_view(), name = "payment"),  
    # path('custom_button/', CustomPayPalPaymentsForm.as_views, name = "custom_button"),  
]