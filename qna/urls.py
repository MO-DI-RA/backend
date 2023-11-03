from django.urls import path
from .views import *

app_name='main'

urlpatterns=[
    path('posts/', ListAPIView.as_view()),
    path('posts/<int:pk>', PostAPIView.as_view())
]
