from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Post, Comment, Like

UserAdmin.fieldsets += ('Custom fields', {'fields': ('profile_pic', 'nickname', 'kakao_id', 'address', 'following',)}),
UserAdmin.inlines = (
    UserInline,
    CommentInline,
    LikeInline,
)
class UserInline():
    
    
class PostAdmin(admin.ModelAdmin):
    inlines = (
        # Inline을 추가해 주세요
    )

class CommentAdmin(admin.ModelAdmin):
    inlines = (
        # Inline을 추가해 주세요
    )

admin.site.register(User, UserAdmin)

admin.site.register(Post, PostAdmin)

admin.site.register(Comment, CommentAdmin)

admin.site.register(Like)