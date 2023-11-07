from rest_framework import serializers

from users.models import User
from .models import QnAPost, Answer


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
        ]


class QnADetailSerializer(serializers.ModelSerializer):
    
    author_nickname = serializers.ReadOnlyField(source="author_id.nickname")
    author_profile_image = serializers.ImageField(
        source="author_id.profile_image", read_only=True
    )
    comments = serializers.SerializerMethodField()

    class Meta:
        model = QnAPost
        fields = [
            "id",
            "author_id",
            "author_nickname",
            "author_profile_image",
            "title",
            "content",
            "comments",
        ]

    def get_comments(self, obj):
        answers = [
            {
                "user": User.objects.get(id=answer.author_id).nickname,
                "content": answer.content,
                "created_at": answer.created_at,
                "updated_at": answer.updated_at,
            }
            for answer in Answer.objects.filter(qna_id=obj.id)
        ]
        return answers

class AnswerSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source="author_id.nickname")

    class Meta:
        model = Answer
        fields = ["id", "writer", "content", "create_at", "updated_at"]