from django.urls import path
<<<<<<< HEAD
from rest_framework_simplejwt.views import TokenRefreshView
=======
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenObtainPairView,
)
>>>>>>> develop
from .views import (
    RegisterAPIView,
    LoginAPIView,
    UserDetailAPIView,
<<<<<<< HEAD
    kakao_callback,
    kakao_login,
=======
    # kakao_callback,
    # kakao_test,
    kakao_login,
    KakaoLogin,
>>>>>>> develop
)

urlpatterns = [
    path("signup/", RegisterAPIView.as_view()),  # post - 회원가입
    path("login/", LoginAPIView.as_view()),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view()),
<<<<<<< HEAD
    path("mypage/", UserDetailAPIView.as_view()),
    path("kakao/login", kakao_login, name="kakao_login"),
    path("kakao/callback", kakao_callback, name="kakao_callback"),
]
=======
    path("verify/", TokenVerifyView.as_view()),
    path("mypage/", UserDetailAPIView.as_view()),
    path("kakao/login/", kakao_login, name="kakao_test"),
    path("kakao/login/finish/", KakaoLogin.as_view()),
    # path("kakao/login/", kakao_test, name="kakao_login"),  # with react
    # path("kakao/callback/", kakao_callback, name="kakao_callback"),
]
>>>>>>> develop
