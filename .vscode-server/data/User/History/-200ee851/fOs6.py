from django.shortcuts import redirect
from allauth.account.utils import send_email_confirmation

# 이메일 확인 요청 후 리다이렉트 함수(confirmation_required_redirect) 정의
def confirmation_required_redirect(self, request):
    send_email_confirmation(request, request.user)  # allauth 패키지의 send_email_confirmation 함수를 호출하여 이메일 확인 메일을 전송
    return redirect("account_email_confirmation_required")  # 이메일 확인이 필요한 페이지로 리다이렉트
