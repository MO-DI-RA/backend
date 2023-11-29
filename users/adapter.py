from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class KakaoSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        oauth_data = sociallogin.account.extra_data.get("kakao_account").get("profile")
        # print("-----------------------------------", oauth_data)
        user.nickname = oauth_data.get("nickname")
        user.save()
        return user
