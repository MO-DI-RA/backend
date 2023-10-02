from django.db import models

# Create your models here.
class Users(models.Model):
    user_id = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    nickname = models.CharField(max_length=20, unique = True)
    password = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now=True)
    