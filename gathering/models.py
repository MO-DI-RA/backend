from django.db import models
from users.models import User


class GatheringPost(models.Model):
    author_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    tag = models.CharField(max_length=10)
    method = models.CharField(max_length=10)
    max_people = models.IntegerField()
    period = models.CharField(max_length=20)
    title = models.CharField(
        verbose_name="title",
        max_length=64,
    )
    content = models.TextField(
        verbose_name="content",
        max_length=2000,
    )
<<<<<<< HEAD
    status = models.BooleanField(verbose_name="status", default=False)
=======
    summary = models.CharField(verbose_name="summary", max_length=50)
    status = models.BooleanField(verbose_name="status", default=False)
    deadline = models.DateTimeField(verbose_name="deadline", null=True)
>>>>>>> develop
    created_at = models.DateTimeField(verbose_name="created at", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="updated at", auto_now=True)


class GatheringLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(GatheringPost, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")  # 한 사용자가 같은 게시물에 중복하여 좋아요를


class Comment(models.Model):
    author_id = models.ForeignKey(
        User,
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
