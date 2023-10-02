from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.contenttypes.admin import GenericStackedInline
from .models import User, Review, Comment, Like

class CommentInline(admin.StackedInline):
    model = Comment
    
class LikeInline(GenericStackedInline):
    model = Like 
    
UserAdmin.fieldsets += ('Custom fields', {'fields': ('nickname', 'profile_pic', 'intro', 'following')}),

admin.site.register(User, UserAdmin)

admin.site.register(Review)

admin.site.register(Comment)

admin.site.register(Like)