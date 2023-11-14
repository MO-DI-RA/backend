from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenObtainPairView,
)
from .views import (
    RegisterAPIView,
    LoginAPIView,
    UserDetailAPIView,
    kakao_callback,
    kakao_login,
    KakaoLogin,
)

urlpatterns = [
    path("signup/", RegisterAPIView.as_view()),  # post - 회원가입
    path("login/", LoginAPIView.as_view()),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view()),
    path("verify/", TokenVerifyView.as_view()),
    path("mypage/", UserDetailAPIView.as_view()),
    path("kakao/login/", kakao_login, name="kakao_login"),
    path("kakao/callback/", kakao_callback, name="kakao_callback"),
    path("kakao/login/finish/", KakaoLogin.as_view()),
]
