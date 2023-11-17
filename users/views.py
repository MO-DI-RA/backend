from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from .serializers import *

import requests


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
            # res.set_cookie("access", access_token, httponly=True)
            # res.set_cookie("refresh", refresh_token, httponly=True)
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

    def put(self, request):  # 프로필 사진 업데이트 닉네임, 유저 프로필 사진만 받아서 put
        if request.user.is_authenticated:
            serializer = UserUpdateSerializers(request.user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"message": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED
            )


# def kakao_test(request):
#     client_id = SOCIAL_AUTH_KAKAO_CLIENT_ID
#     return redirect(
#         f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code"
#     )
#
#
# def kakao_callback(request):
#     client_id = SOCIAL_AUTH_KAKAO_CLIENT_ID
#     code = request.GET.get("code")
#     print(code)
#     token_request = requests.get(
#         f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={KAKAO_CALLBACK_URI}&code={code}",
#     )
#     return JsonResponse(token_request.json())

# .env 파일로 숨겨야함

SOCIAL_AUTH_KAKAO_CLIENT_ID = "e1e4af98ca9f6131da2d779f616737bc"
SOCIAL_AUTH_KAKAO_SECRET = "977163"
KAKAO_CALLBACK_URI = "http://127.0.0.1:3000/user/kakao/callback/"


def kakao_login(request):
    client_id = SOCIAL_AUTH_KAKAO_CLIENT_ID

    code = request.GET["code"]  # code 쿼리스트링을 찾아서
    token_request = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={KAKAO_CALLBACK_URI}&code={code}",
    )
    token_response_json = token_request.json()
    access_token = token_response_json.get("access_token")
    code_error_msg = token_response_json.get("error")

    if code_error_msg:  # 거의 대부분의 상황이 code가 만료나 중복
        return JsonResponse({"err_msg": "failed to signin"})

    profile_request = requests.post(
        "https://kapi.kakao.com/v2/user/me",
        headers={
            "Authorization": f"bearer {access_token}",
        },
    )

    profile_json = profile_request.json()
    kakao_account = profile_json.get("kakao_account")
    email = kakao_account.get("email", None)

    print(email)

    try:
        user = User.objects.get(email=email)
        social_user = SocialAccount.objects.get(user=user)

        if social_user.provider != "kakao":
            return JsonResponse(
                {"err_msg": "no matching social type"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = {"access_token": access_token, "code": code}

        accept = requests.post(
            "http://localhost:8000/user/kakao/login/finish/", data=data
        )
        accept_status = accept.status_code
        # print(accept_status)

        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signin"}, status=accept_status)

        accept_json = accept.json()
        print(accept_json)
        print("Login 성공")
        accept_json.pop("user", None)
        return JsonResponse(accept_json)

    except User.DoesNotExist:
        # 전달받은 이메일로 기존에 가입된 유저가 아예 없으면 => 새로 회원가입 & 해당 유저의 jwt 발급
        data = {"access_token": access_token, "code": code}
        accept = requests.post(
            "http://localhost:8000/user/kakao/login/finish/", data=data
        )
        print(accept)
        accept_status = accept.status_code

        # 뭔가 중간에 문제가 생기면 에러
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signup"}, status=accept_status)

        accept_json = accept.json()
        accept_json.pop("user", None)
        print(accept_json)
        print("Kakao 회원가입 성공")
        return JsonResponse(accept_json)

    except SocialAccount.DoesNotExist:
        # User는 있는데 SocialAccount가 없을 때 (=일반회원으로 가입된 이메일일때)
        return JsonResponse(
            {"err_msg": "email exists but not social user"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    callback_url = KAKAO_CALLBACK_URI
    client_class = OAuth2Client
