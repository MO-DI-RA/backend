from django.urls import path
from .views import *

app_name='main'

urlpatterns=[
    path('',index),
    path('test1/',gathering),
]