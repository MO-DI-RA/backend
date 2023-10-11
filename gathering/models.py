from django.db import models
<<<<<<< HEAD
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,  # superuser 라는 권한이 생겼기 때문에 추가해 줘야함
)


# User model 을 위한 헬퍼 클래스
class UserManager(BaseUserManager):
    def create_user(self, email, password, nickname, **kwargs):
        if not email:
            raise ValueError("User must have email address")

        user = self.model(email=email, nickname=nickname)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password, nickname, **extra_fields):
        superuser = self.create_user(
            email=email,
            password=password,
            nickname=nickname,
        )
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True

        superuser.save(using=self._db)
        return superuser

    def __str__(self):
        return self.nickname


# User model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=50, unique=True, null=False, blank=False
    )  # email
    nickname = models.CharField(
        max_length=20, unique=True, null=False, blank=False
    )  # nickname
    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    is_superuser = models.BooleanField(default=False)
    
    user_created_at = models.DateTimeField(auto_now=True)

    objects = UserManager()  # 헬퍼 클래스 지정

    USERNAME_FIELD = "email"  # email로 로그인 설정

    REQUIRED_FIELDS = [  # USERNAME_FIELD, Password는 항상 기본적으로 요구 따로 명시 x
        "nickname",
    ]
=======
from users.models import User


class GatheringPost(models.Model):
    author_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        verbose_name="title",
        max_length=64,
    )
    content = models.TextField(
        verbose_name="content",
        max_length=2000,
    )
    created_at = models.DateTimeField(verbose_name="created at", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="updated at", auto_now=True)


class Comment(models.Model):
    author_id = models.ForeignKey(
        User,
        related_name="users",
        on_delete=models.CASCADE,
    )
    post_id = models.ForeignKey(
        GatheringPost, verbose_name="gatherings", on_delete=models.CASCADE
    )
    content = models.CharField(
        verbose_name="comment",
        max_length=300,
    )
    created_at = models.DateTimeField(verbose_name="created at", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="updated at", auto_now=True)
>>>>>>> 1b3a0aa38059994d474bba1e3ca59857888f4fdc
