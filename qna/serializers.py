from rest_framework import serializers

from users.models import User
<<<<<<< HEAD
from .models import QnAPost, Answer, AnswerComment
=======
from .models import QnAPost, Answer, AnswerComment, InterestedPost, Like
>>>>>>> develop


class QnAListSerializer(serializers.ModelSerializer):
    author_nickname = serializers.ReadOnlyField(source="author_id.nickname")

    author_profile_image = serializers.ImageField(
        source="author_id.profile_image", read_only=True
    )
    # print(author_profile_image)
<<<<<<< HEAD
=======
    # auther_id = serializers.IntegerField(source="author_id", read_only=True)
>>>>>>> develop

    class Meta:
        model = QnAPost
        fields = [
            "id",
<<<<<<< HEAD
            "author_id",
=======
            # "author_id",
>>>>>>> develop
            "author_profile_image",
            "author_nickname",
            "title",
            "content",
            "created_at",
            "status",
        ]


<<<<<<< HEAD
=======
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "post"]


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestedPost
        fields = ["post", "id"]


>>>>>>> develop
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
<<<<<<< HEAD
            "author_id",
=======
            # "author_id",
>>>>>>> develop
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
<<<<<<< HEAD
=======
                "answer_id": answer.id,
>>>>>>> develop
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
<<<<<<< HEAD
            "author_id",
=======
            # "author_id",
>>>>>>> develop
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
<<<<<<< HEAD
                # "author_profile_image" : AnswerComment.author_id.profile_image, 보류
=======
                # "author_profile_image" : AnswerComment.author_id.profile_image,
>>>>>>> develop
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

<<<<<<< HEAD
=======
    #
>>>>>>> develop
    class Meta:
        model = AnswerComment
        fields = [
            "id",
            "answer_id",
<<<<<<< HEAD
            "author_id",
=======
            # "author_id",
>>>>>>> develop
            "writer",
            "author_profile_image",
            "content",
            "created_at",
            "updated_at",
<<<<<<< HEAD
        ]
=======
        ]


#
>>>>>>> develop
