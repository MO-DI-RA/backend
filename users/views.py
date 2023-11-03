from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.shortcuts import redirect

from allauth.socialaccount.providers.kakao import views as kakao_views
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
import requests
from json import JSONDecodeError
from django.http import JsonResponse


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register successs",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )

            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            # print(res)
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        # 유저 인증
        user = authenticate(
            email=request.data.get("email"), password=request.data.get("password")
        )
        # 이미 회원가입 된 유저일 때
        if user is not None:
            serializer = UserSerializer(user)
            print(serializer.data)
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "login success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            # jwt 토큰 => 쿠키에 저장
            # print(refresh_token)
            # res.set_cookie("access", access_token, httponly=True)
            # res.set_cookie("refresh", refresh_token, httponly=True)
            print(res)
            return res
        else:
            return Response(
                {"message": "등록되지 않은 아이디 입니다."}, status=status.HTTP_400_BAD_REQUEST
            )


class UserDetailAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED
            )


SOCIAL_AUTH_KAKAO_CLIENT_ID = "e1e4af98ca9f6131da2d779f616737bc"
SOCIAL_AUTH_KAKAO_SECRET = "977163"
KAKAO_CALLBACK_URI = "http://localhost:8000/user/kakao/callback"


def kakao_login(request):
    client_id = SOCIAL_AUTH_KAKAO_CLIENT_ID
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code&scope=account_email"
    )


def kakao_callback(request):
    client_id = SOCIAL_AUTH_KAKAO_CLIENT_ID
    code = request.GET.get("code")
    print(code)
    # code로 access token 요청
    token_request = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={KAKAO_CALLBACK_URI}&code={code}"
    )
    token_response_json = token_request.json()
    return JsonResponse(data=token_response_json, status=status.HTTP_200_OK)


#  sy99Bb99LzH8U04fM_fPl6S_JH4nUIDQ4zsKKclgAAABi5Ug_4KYFzyUYZmfhQ

#
#     # 에러 발생 시 중단
#     error = token_response_json.get("error", None)
#     if error is not None:
#         raise JSONDecodeError(error)
#
#     access_token = token_response_json.get("access_token")
#
#     profile_request = requests.post(
#         "https://kapi.kakao.com/v2/user/me",
#         headers={"Authorization": f"Bearer {access_token}"},
#     )
#     profile_json = profile_request.json()
#
#     kakao_account = profile_json.get("kakao_account")
#     email = kakao_account.get("email", None)  # 이메일!
#     print(profile_json)
#     # return Response(data=profile_json)
