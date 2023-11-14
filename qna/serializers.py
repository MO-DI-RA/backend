from rest_framework import serializers

from users.models import User
from .models import QnAPost, Answer, AnswerComment


class QnAListSerializer(serializers.ModelSerializer):
    author_nickname = serializers.ReadOnlyField(source="author_id.nickname")

    author_profile_image = serializers.ImageField(
        source="author_id.profile_image", read_only=True
    )
    # print(author_profile_image)

    class Meta:
        model = QnAPost
        fields = [
            "id",
            "author_id",
            "author_profile_image",
            "author_nickname",
            "title",
            "content",
            "created_at",
            "status",
        ]


class QnADetailSerializer(serializers.ModelSerializer):
    author_nickname = serializers.ReadOnlyField(source="author_id.nickname")
    author_profile_image = serializers.ImageField(
        source="author_id.profile_image", read_only=True
    )
    answers = serializers.SerializerMethodField()

    class Meta:
        model = QnAPost
        fields = [
            "id",
            "author_id",
            "author_nickname",
            "author_profile_image",
            "title",
            "content",
            "answers",
            "status",
        ]

    def get_answers(self, obj):
        answers = [
            {
                "author_nickname": answer.author_id.nickname,
                # "author_profile_image" : comment.author_id.profile_image, 보류,
                "content": answer.content,
                "created_at": answer.created_at,
                "updated_at": answer.updated_at,
            }
            for answer in Answer.objects.filter(qna_id=obj.id)
        ]
        return answers


class AnswerSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source="author_id.nickname")
    author_profile_image = serializers.ImageField(
        source="author_id.profile_image", read_only=True
    )
    answercomments = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = [
            "id",
            "qna_id",
            "author_id",
            "writer",
            "author_profile_image",
            "content",
            "answercomments",
            "created_at",
            "updated_at",
        ]

    def get_answercomments(self, obj):
        comments = [
            {
                "author_nickname": AnswerComment.author_id.nickname,
                # "author_profile_image" : AnswerComment.author_id.profile_image, 보류
                "content": AnswerComment.content,
                "created_at": AnswerComment.created_at,
                "updated_at": AnswerComment.updated_at,
            }
            for AnswerComment in AnswerComment.objects.filter(answer_id=obj.id)
        ]
        return comments


class AnswerCommentSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source="author_id.nickname")
    author_profile_image = serializers.ImageField(
        source="author_id.profile_image", read_only=True
    )

    class Meta:
        model = AnswerComment
        fields = [
            "id",
            "answer_id",
            "author_id",
            "writer",
            "author_profile_image",
            "content",
            "created_at",
            "updated_at",
        ]