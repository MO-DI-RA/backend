from rest_framework import serializers

from users.models import User
from qna.models import QnA, Answer


class QnAListSerializer(serializers.ModelSerializer):
    author_nickname = serializers.ReadOnlyField(source="author_id.nickname")

    author_profile_image = serializers.ImageField(
        source="author_id.profile_image", read_only=True
    )
    # print(author_profile_image)

    class Meta:
        model = QnA
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
        model = QnA
        fields = [
            "id",
            "author_id",
            "author_nickname",
            "author_profile_image",
            "title",
            "content",
            "comments",
        ]

    def get_answers(self, obj):
        answers = [
            {
                "user": User.objects.get(id=answear.author_id).nickname,
                "content": answear.content,
                "created_at": answear.created_at,
                "updated_at": answear.updated_at,
            }
            for answear in Answer.objects.filter(post_id=obj.id)
        ]
        return answers

class AnswerSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source="author_id.nickname")

    class Meta:
        model = Answer
        fields = ["id", "writer", "content", "create_at", "updated_at"]
