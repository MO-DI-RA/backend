from .models import User
from rest_framework import serializers
from dj_rest_auth.registration.serializers import SocialLoginSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "profile_image", "nickname"]

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            nickname=validated_data["nickname"],
        )
        return user


<<<<<<< HEAD
=======
class UserUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["nickname", "profile_image"]


>>>>>>> develop
class KaKaoSocialSerializer(SocialLoginSerializer):
    def custom_save(self, request, sociallogin):
        user = sociallogin.user
        extra_data = sociallogin.account.extra_data["kakao_account"]["profile"]
<<<<<<< HEAD
        print("여기가 출력분 입니다. ", extra_data)
        user.nickname = extra_data["nickname"]
        user.profile_image = extra_data["profile_image_url"]
        user.save()
=======
        # print("여기가 출력분 입니다. ", extra_data)
        user.nickname = extra_data["nickname"]
        user.profile_image = extra_data["profile_image_url"]  # profile 딱히 필요 없을듯
        user.save()
>>>>>>> develop
