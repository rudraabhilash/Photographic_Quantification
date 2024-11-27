from django.urls import path
from . import views

urlpatterns = [path('doctor/', views.doctor, name = 'doctor'),
               path('doctordata/', views.doctordata, name = 'doctordata'),]