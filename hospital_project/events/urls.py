from django.urls import path
from . import views

urlpatterns = [path('', views.event1, name = 'event1'),]
