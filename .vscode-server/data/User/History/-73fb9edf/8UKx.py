from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    nickname = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        error_messages={'unique': '이미 사용중인 닉네임입니다.'}
    )

    kakao_id = models.CharField(max_length=20, null=True)

    address = models.CharField(max_length=40, null=True)

    def __str__(self):
        return self.email
