from rest_framework import serializers

from users.models import User
from .models import GatheringPost, Comment


class PostCreateSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source="users.nickname")

    class Meta:
        model = GatheringPost
        fields = ["title", "writer", "content"]


class PostListSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source="users.nickname")

    class Meta:
        model = GatheringPost
        fields = ["id", "title", "writer", "created_at"]


class PostDetailSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source="users.nickname")
    comments = serializers.SerializerMethodField()

    class Meta:
        model = GatheringPost
        fields = ["id", "title", "writer", "content", "comments"]

    def get_comments(self, obj):
        comments = [
            {
                "user": User.objects.get(id=comment.author_id).nickname,
                "content": comment.content,
                "created_at": comment.create_at,
                "updated_at": comment.updated_at,
            }
            for comment in Comment.objects.filter(post_id=obj.id)
        ]
        return comments


class CommentSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source="users.nickname")

    class Meta:
        model = Comment
        fields = ["id", "writer", "content", "create_at", "updated_at"]
