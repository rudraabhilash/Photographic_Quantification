from django.urls import path
from . import views

urlpatterns = [path('payment', views.payment, name = 'payment'),
               path('paymentsdata', views.paymentsdata, name = 'paymentsdata'),
               path('paymentsdatawrite', views.paymentsdatawrite, name='paymentsdatawrite'),
               path('paymentsdata', views.paymentsdata, name='paymentsdata'),]

