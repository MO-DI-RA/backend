from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_no_special_characters

# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(
        max_length=15,
        unique =True,
        null=True,
        validators = [validate_no_special_characters],
        error_messages={"unique":"이미 사용중인 닉네임입니다"},
    )
    
    
    def __str__(self):
        return self.email

class Review(models.Model):
    title = models.CharField(max_length=30)
    restaurant_name = models.CharField(max_length=20)
    restaurant_link = models.URLField()
    title = models.CharField(max_length=30)