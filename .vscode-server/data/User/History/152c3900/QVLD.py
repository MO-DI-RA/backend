from django.db import models
from .validators import validate_email, validate_password

# Create your models here.
class Users(models.Model):
    user_id = models.CharField(max_length=20)
    email = models.EmailField(validators=[validate_email])
    nickname = models.CharField(max_length=20, unique = True)
    password = models.CharField(max_length=20, validators=[validate_password])
    created_at = models.DateTimeField(auto_now=True)

