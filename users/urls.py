from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterAPIView, LoginAPIView, UserDetailAPIView

urlpatterns = [
    path("signup/", RegisterAPIView.as_view()),  # post - 회원가입
    path("login/", LoginAPIView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("mypage/", UserDetailAPIView.as_view()),
]
