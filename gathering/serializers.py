from rest_framework import serializers

from users.models import User
from gathering.models import GatheringPost, Comment, GatheringLike


class PostListSerializer(serializers.ModelSerializer):
    author_nickname = serializers.ReadOnlyField(source="author_id.nickname")

    author_profile_image = serializers.ImageField(
        source="author_id.profile_image", read_only=True
    )
    # print(author_profile_image)

    class Meta:
        model = GatheringPost
        fields = [
            "id",
            # "author_id",
            "contact",
            "division",
            "author_profile_image",
            "author_nickname",
            "deadline",
            "title",
            "content",
            "created_at",
            "status",
            "summary",
            "tag",
            "method",
            "max_people",
            "period",
        ]


class PostDetailSerializer(serializers.ModelSerializer):
    author_nickname = serializers.ReadOnlyField(source="author_id.nickname")
    author_profile_image = serializers.ImageField(
        source="author_id.profile_image", read_only=True
    )
    comments = serializers.SerializerMethodField()
    author_id = serializers.PrimaryKeyRelatedField(read_only=True)  # 이거 여기 저기 추가 해줘야함

    class Meta:
        model = GatheringPost
        fields = [
            "id",
            "author_id",
            "author_nickname",
            "author_profile_image",
            "deadline",
            "title",
            "content",
            "contact",
            "comments",
            "status",
            "tag",
            "method",
            "max_people",
            "period",
        ]

    def get_comments(self, obj):
        comments = [
            {
                "author_nickname": comment.author_id.nickname,
                # "author_profile_image": comment.author_id.profile_image,  # 보류
                "content": comment.content,
                "created_at": comment.created_at,
                "updated_at": comment.updated_at,
            }
            for comment in Comment.objects.filter(post_id=obj.id)
        ]
        # print(comments)
        return comments


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GatheringLike
        fields = ["id", "post"]


class CommentSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source="author_id.nickname")
    author_profile_image = serializers.ImageField(
        source="author_id.profile_image", read_only=True
    )
    author_id = serializers.PrimaryKeyRelatedField(read_only=True)  # 이거 여기 저기 추가 해줘야함

    class Meta:
        model = Comment
        fields = [
            "id",
            "author_id",
            "writer",
            "author_profile_image",
            "content",
            "created_at",
            "updated_at",
        ]
