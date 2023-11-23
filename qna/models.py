from django.db import models
from users.models import User


class QnAPost(models.Model):
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
    status = models.BooleanField(verbose_name="status", default=False)
    created_at = models.DateTimeField(verbose_name="created at", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="updated at", auto_now=True)


class Answer(models.Model):
    author_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    qna_id = models.ForeignKey(QnAPost, verbose_name="qnas", on_delete=models.CASCADE)
    content = models.CharField(
        verbose_name="answer",
        max_length=300,
    )
    created_at = models.DateTimeField(verbose_name="created at", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="updated at", auto_now=True)


class AnswerComment(models.Model):
    author_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    answer_id = models.ForeignKey(
        Answer, verbose_name="answers", on_delete=models.CASCADE
    )
    content = models.CharField(
        verbose_name="answercomment",
        max_length=300,
    )
    created_at = models.DateTimeField(verbose_name="created at", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="updated at", auto_now=True)
