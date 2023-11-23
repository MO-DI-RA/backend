from django.contrib import admin
from .models import QnAPost, Answer, InterestedPost

# Register your models here.
admin.site.register(QnAPost)
admin.site.register(Answer)
admin.site.register(InterestedPost)
