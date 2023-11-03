from django.urls import path
from .views import *


urlpatterns=[
    path('posts/', ListAPIView.as_view()),
    path('posts/<int:pk>', PostAPIView.as_view())
]
