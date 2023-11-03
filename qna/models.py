from django.db import models
from users.models import User


class QnA(models.Model):
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

class Answer(models.Model):
    author_id = models.ForeignKey(
        User,
        related_name="responsers",
        on_delete=models.CASCADE,
    )
    qna_id = models.ForeignKey(
        QnA, verbose_name="qnas", on_delete=models.CASCADE
    )
    content = models.CharField(
        verbose_name="answer",
        max_length=300,
    )
    created_at = models.DateTimeField(verbose_name="created at", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="updated at", auto_now=True)
