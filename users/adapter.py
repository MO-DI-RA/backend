from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class KakaoSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        oauth_data = sociallogin.account.extra_data.get("kakao_account").get("profile")
        # print("-----------------------------------", oauth_data)
        user.nickname = oauth_data.get("nickname")
        user.profile_image = oauth_data.get(
            "profile_image_url"
        )  # 뭔가 이상하게 url이 파싱됨 이미지는 저장 안해도 될지도
        user.save()
        return user
