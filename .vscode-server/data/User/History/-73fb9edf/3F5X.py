from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    nickname = CharField(max_length=15, unique = True)
    kakao_id = CharField(max_length=20)
    address = CharField(max_length=40)
    def __str__(self):
        return self.email