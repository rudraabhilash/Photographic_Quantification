from django.urls import path
from . import views

urlpatterns = [path('payment', views.payment, name = 'payment'),
               path('paymentsdata', views.paymentsdata, name = 'paymentsdata'),]

