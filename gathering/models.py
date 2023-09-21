from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# User model 을 위한 헬퍼 클래스
class UserManager(BaseUserManager):
    def create_user(self, email, password, nickname, **kwargs):
        user = self.model(email=email, nickname=nickname)
        user.set_password(password)
        user.save(using=self.db)
        return user


# User model
class User(AbstractBaseUser):
    pass
