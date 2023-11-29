from .models import QnAPost, Answer, AnswerComment, InterestedPost, Like
from .serializers import (
    QnADetailSerializer,
    QnAListSerializer,
    AnswerSerializer,
    AnswerCommentSerializer,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics


class ListAPIView(APIView):  ## auther_id 도 나와야함
    def get(self, request):  # 모든 게시물
        posts = QnAPost.objects.all()
        serializer = QnAListSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.is_authenticated:
            serializer = QnAListSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author_id_id=request.user.id)  # 이런식으로 바꿔줘
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


# post
class PostAPIView(APIView):
    def get_object(self, pk):
        try:
            return QnAPost.objects.get(pk=pk)
        except QnAPost.DoesNotExist:
            raise Http404

    # CRUD 중 R
    def get(self, request, pk, format=None):
        if not request.user.is_authenticated:
            post = self.get_object(pk)
            serializer = QnADetailSerializer(post)
            data = serializer.data
            data["like_status"] = False
            return Response(data=data)
        else:
            like = Like.objects.filter(post=pk, user=request.user.id)
            if like:
                post = self.get_object(pk)
                serializer = QnADetailSerializer(post)
                data = serializer.data
                data["like_status"] = True
                return Response(data=data)
            else:
                post = self.get_object(pk)
                serializer = QnADetailSerializer(post)
                data = serializer.data
                data["like_status"] = False
                return Response(data=data)

    # CRUD 중 U
    def put(self, request, pk, format=None):
        if request.user.is_authenticated:
            post = self.get_object(pk)
            if post.author_id.id == request.user.id:  # 작성자가 같을때만 수정 가능
                serializer = QnADetailSerializer(post, data=request.data)
                if serializer.is_valid():
                    serializer.save(author_id_id=request.user.id)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "자신의 게시물이 아닙니다."}, status=status.HTTP_403_FORBIDDEN
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    # CRUD 중 D
    def delete(self, request, pk, format=None):
        if request.user.is_authenticated:
            post = self.get_object(pk)
            if post.author_id.id == request.user.id:  # 작성자가 같을때만 삭제 가능
                post.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {"message": "자신의 게시물이 아닙니다."}, status=status.HTTP_403_FORBIDDEN
                )
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class PostViewSet(generics.ListAPIView):  # Search by title
    queryset = QnAPost.objects.all()
    serializer_class = QnADetailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["title"]


class LikeAPIView(APIView):
    def post(self, request, post_id):
        if request.user.is_authenticated:
            user = request.user
            post = QnAPost.objects.get(id=post_id)  # 있는지 없는지 처리 해야함
            print(post)
            print(user)
            # 이미 좋아요가 눌렸는지 확인
            like, created = Like.objects.get_or_create(user=user, post=post)
            if not created:
                # 이미 좋아요가 되어있다면 제거
                like.delete()
                return Response(
                    {"message": "좋아요가 취소되었습니다."}, status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response({"message": "좋아요!"}, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class LikeDeleteView(APIView):
    def delete(self, request):
        if request.user.is_authenticated:
            likes_id = request.data
            print(likes_id)
            for id in likes_id:
                like = Like.objects.get(post=id)
                like.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class LikeStatusView(APIView):
    def get(self, request, post_id):
        print(request.user)
        if request.user.is_authenticated:
            like = Like.objects.filter(post=post_id, user=request.user.id)
            if like:
                return Response(data=True)
            else:
                # print("-------------", like)
                return Response(data=False)
        else:
            # print("tlqkf")
            return Response(data=False)


class UserPostAPIView(APIView):
    def get(self, request):
        user_id = request.user.id
        posts = QnAPost.objects.filter(author_id=user_id)
        serializer = QnAListSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserInterestListAPI(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            likes = Like.objects.filter(user=user)
            liked_posts = QnAPost.objects.filter(
                id__in=likes.values_list("post", flat=True)
            )
            serializer = QnAListSerializer(liked_posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            Response(status=status.HTTP_401_UNAUTHORIZED)


class PostToggleStatus(APIView):
    def get_object(self, pk):
        try:
            return QnAPost.objects.get(pk=pk)
        except QnAPost.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        if request.user.is_authenticated:
            post = self.get_object(pk)
            if post.author_id.id == request.user.id:
                post.status = not post.status
                post.save()
                return Response(
                    {"message": "게시물 상태가 토글되었습니다."}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"message": "자신의 게시물이 아닙니다."}, status=status.HTTP_403_FORBIDDEN
                )
        else:
            Response(status=status.HTTP_401_UNAUTHORIZED)


class AnswerAPIView(APIView):
    def get_object(self, pk):
        try:
            return Answer.objects.get(pk=pk)
        except Answer.DoesNotExist:
            raise Http404

    # CRUD 중 R
    def get(self, request, pk, comment_pk, format=None):
        comment = self.get_object(comment_pk)
        serializer = AnswerSerializer(comment)
        print(serializer)
        return Response(serializer.data)

    # CRUD 중 U
    def put(self, request, pk, comment_pk, format=None):
        comment = self.get_object(comment_pk)
        # print(request.user.id)
        if comment.author_id.id == request.user.id:  # 작성자가 같을때만 수정 가능
            serializer = AnswerSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save(author_id_id=request.user.id)
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "자신의 답변이 아닙니다."}, status=status.HTTP_403_FORBIDDEN
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # CRUD 중 D
    def delete(self, request, pk, comment_pk, format=None):
        comment = self.get_object(comment_pk)
        if comment.author_id.id == request.user.id:  # 작성자가 같을때만 삭제 가능
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"message": "자신의 댓글이 아닙니다."}, status=status.HTTP_403_FORBIDDEN
            )


class AnswerListAPIView(APIView):  ## auther_id 도 나와야함
    def get(self, request, pk):  # 모든 게시물
        comments = Answer.objects.all().filter(qna_id=pk)
        serializer = AnswerSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        if request.user.is_authenticated:
            serializer = AnswerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author_id_id=request.user.id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class AnswerCommentAPIView(APIView):
    def get_object(self, pk):
        try:
            return AnswerComment.objects.get(pk=pk)
        except AnswerComment.DoesNotExist:
            raise Http404

    # CRUD 중 R
    def get(self, request, pk, comment_pk, reply_pk, format=None):
        comment = self.get_object(reply_pk)
        serializer = AnswerCommentSerializer(comment)
        return Response(serializer.data)

    # CRUD 중 U
    def put(self, request, pk, comment_pk, reply_pk, format=None):
        if request.user.is_authenticated:
            comment = self.get_object(reply_pk)
            # print(request.user.id)
            if comment.author_id.id == request.user.id:  # 작성자가 같을때만 수정 가능
                serializer = AnswerCommentSerializer(comment, data=request.data)
                if serializer.is_valid():
                    serializer.save(author_id_id=request.user.id)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "자신의 댓글이 아닙니다."}, status=status.HTTP_403_FORBIDDEN
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    ## 자기거만 삭제
    # CRUD 중 D
    def delete(self, request, pk, comment_pk, reply_pk, format=None):
        if request.user.is_authenticated:
            comment = self.get_object(reply_pk)
            if comment.author_id.id == request.user.id:  # 작성자가 같을때만 삭제 가능
                comment.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {"message": "자신의 댓글이 아닙니다."}, status=status.HTTP_403_FORBIDDEN
                )
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


#
class AnswerCommentListAPIView(APIView):  ## auther_id 도 나와야함
    def get(self, request, pk, comment_pk):  # 모든 게시물
        comments = AnswerComment.objects.all().filter(answer_id=comment_pk)
        serializer = AnswerCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk, comment_pk):
        if request.user.is_authenticated:
            print(request)
            serializer = AnswerCommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author_id_id=request.user.id, answer_id_id=comment_pk)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
