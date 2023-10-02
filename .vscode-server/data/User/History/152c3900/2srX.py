from django.db import models
from .validators import validate_email, validate_password

# Create your models here.
class Users(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    email = models.EmailField(validators=[validate_email])
    nickname = models.CharField(max_length=20, unique = True)
    password = models.CharField(max_length=20, validators=[validate_password])
    created_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    author_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    content = models.TextField(max_length=150)
    post_id = models.IntegerField(max_length=30)
    created_at = models.DateTimeField(auto_now=True)