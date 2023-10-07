from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=300, blank=True)
    user_id = models.IntegerField(unique=True)
    status = models.CharField(max_length=30)
    post_created_at = models.DateTimeField(auto_now_add=True)
    
    def __str(self):
        return self.title

class Comment(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    comment_created_at = models.DateTimeField(auto_now_add=True)
    