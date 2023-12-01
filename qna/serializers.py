from rest_framework import serializers

from users.models import User
from .models import QnAPost, Answer, AnswerComment, InterestedPost, Like


class QnAListSerializer(serializers.ModelSerializer):
    author_nickname = serializers.ReadOnlyField(source="author_id.nickname")

    author_profile_image = serializers.ImageField(
        source="author_id.profile_image", read_only=True, use_url=False
    )
    # print(author_profile_image)
    # auther_id = serializers.IntegerField(source="author_id", read_only=True)
    # author_id = serializers.PrimaryKeyRelatedField(read_only=True)  # 이거 여기 저기 추가 해줘야함

    class Meta:
        model = QnAPost
        fields = [
            "id",
            # "author_id",
            "author_profile_image",
            "author_nickname",
            "title",
            # "summary",
            "content",
            "created_at",
            "status",
        ]


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "post"]


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestedPost
        fields = ["post", "id"]


class QnADetailSerializer(serializers.ModelSerializer):
    author_nickname = serializers.ReadOnlyField(source="author_id.nickname")
    author_profile_image = serializers.ImageField(
        source="author_id.profile_image", read_only=True
    )
    answers = serializers.SerializerMethodField()
    author_id = serializers.PrimaryKeyRelatedField(read_only=True)  # 이거 여기 저기 추가 해줘야함

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
            "created_at",
        ]

    def get_answers(self, obj):
        answers = [
            {
                "answer_id": answer.id,
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
    # answercomments = serializers.SerializerMethodField()
    author_id = serializers.PrimaryKeyRelatedField(read_only=True)  # 이거 여기 저기 추가 해줘야함
    qna_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Answer
        fields = [
            "id",
            "qna_id",
            "author_id",
            "writer",
            "author_profile_image",
            "content",
            # "answercomments",
            "created_at",
            "updated_at",
        ]

    # def get_answercomments(self, obj):
    #     comments = [
    #         {
    #             "author_nickname": AnswerComment.author_id.nickname,
    #             # "author_profile_image": AnswerComment.author_id.profile_image,
    #             "content": AnswerComment.content,
    #             "created_at": AnswerComment.created_at,
    #             "updated_at": AnswerComment.updated_at,
    #         }
    #         for AnswerComment in AnswerComment.objects.filter(answer_id=obj.id)
    #     ]
    #     return comments


class AnswerCommentSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source="author_id.nickname")
    author_profile_image = serializers.ImageField(
        source="author_id.profile_image", read_only=True
    )
    author_id = serializers.PrimaryKeyRelatedField(read_only=True)  # 이거 여기 저기 추가 해줘야함

    #
    class Meta:
        model = AnswerComment
        fields = [
            "id",
            "author_id",
            "writer",
            "author_profile_image",
            "content",
            "created_at",
            "updated_at",
        ]
