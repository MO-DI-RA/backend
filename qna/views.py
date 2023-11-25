<<<<<<< HEAD
from .models import QnAPost, Answer, AnswerComment
=======
from .models import QnAPost, Answer, AnswerComment, InterestedPost, Like
>>>>>>> develop
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
<<<<<<< HEAD
=======
from rest_framework.filters import SearchFilter
from rest_framework import generics
>>>>>>> develop


class ListAPIView(APIView):  ## auther_id 도 나와야함
    def get(self, request):  # 모든 게시물
        posts = QnAPost.objects.all()
        serializer = QnAListSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
<<<<<<< HEAD
        serializer = QnAListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
=======
        if request.user.is_authenticated:
            serializer = QnAListSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author_id_id=request.user.id)  # 이런식으로 바꿔줘
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
>>>>>>> develop


# post
class PostAPIView(APIView):
    def get_object(self, pk):
        try:
            return QnAPost.objects.get(pk=pk)
        except QnAPost.DoesNotExist:
            raise Http404

    # CRUD 중 R
    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = QnADetailSerializer(post)
        return Response(data=serializer.data)

    # CRUD 중 U
    def put(self, request, pk, format=None):
<<<<<<< HEAD
        post = self.get_object(pk)
        if post.author_id.id == request.user.id:  # 작성자가 같을때만 수정 가능
            serializer = QnADetailSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "자신의 게시물이 아닙니다."}, status=status.HTTP_403_FORBIDDEN
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # CRUD 중 D
    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        if post.author_id.id == request.user.id:  # 작성자가 같을때만 삭제 가능
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"message": "자신의 게시물이 아닙니다."}, status=status.HTTP_403_FORBIDDEN
            )
=======
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


class PostViewSet(generics.ListAPIView):
    queryset = QnAPost.objects.all()
    serializer_class = QnADetailSerializer
    filter_backends = [SearchFilter]
    search_fields = ["title"]


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
>>>>>>> develop


class PostToggleStatus(APIView):
    def get_object(self, pk):
        try:
            return QnAPost.objects.get(pk=pk)
        except QnAPost.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
<<<<<<< HEAD
        post = self.get_object(pk)
        if post.author_id.id == request.user.id:
            post.status = not post.status
            post.save()
            return Response({"message": "게시물 상태가 토글되었습니다."}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "자신의 게시물이 아닙니다."}, status=status.HTTP_403_FORBIDDEN
            )
=======
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
>>>>>>> develop


class AnswerAPIView(APIView):
    def get_object(self, pk):
        try:
            return Answer.objects.get(pk=pk)
        except Answer.DoesNotExist:
            raise Http404

    # CRUD 중 R
<<<<<<< HEAD
    def get(self, request, pk, format=None):
        comment = self.get_object(pk)
        serializer = AnswerSerializer(comment)
        return Response(serializer.data)

    # CRUD 중 U
    def put(self, request, pk, format=None):
        comment = self.get_object(pk)
=======
    def get(self, request, pk, comment_pk, format=None):
        comment = self.get_object(comment_pk)
        serializer = AnswerSerializer(comment)
        print(serializer)
        return Response(serializer.data)

    # CRUD 중 U
    def put(self, request, pk, comment_pk, format=None):
        comment = self.get_object(comment_pk)
>>>>>>> develop
        # print(request.user.id)
        if comment.author_id.id == request.user.id:  # 작성자가 같을때만 수정 가능
            serializer = AnswerSerializer(comment, data=request.data)
            if serializer.is_valid():
<<<<<<< HEAD
                serializer.save()
=======
                serializer.save(author_id_id=request.user.id)
>>>>>>> develop
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "자신의 답변이 아닙니다."}, status=status.HTTP_403_FORBIDDEN
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # CRUD 중 D
<<<<<<< HEAD
    def delete(self, request, pk, format=None):
        comment = self.get_object(pk)
=======
    def delete(self, request, pk, comment_pk, format=None):
        comment = self.get_object(comment_pk)
>>>>>>> develop
        if comment.author_id.id == request.user.id:  # 작성자가 같을때만 삭제 가능
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"message": "자신의 댓글이 아닙니다."}, status=status.HTTP_403_FORBIDDEN
            )


class AnswerListAPIView(APIView):  ## auther_id 도 나와야함
<<<<<<< HEAD
    def get(self, request):  # 모든 게시물
        comments = Answer.objects.all()
=======
    def get(self, request, pk):  # 모든 게시물
        comments = Answer.objects.all().filter(qna_id=pk)
>>>>>>> develop
        serializer = AnswerSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
<<<<<<< HEAD
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
=======
        if request.user.is_authenticated:
            serializer = AnswerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author_id_id=request.user.id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
>>>>>>> develop


class AnswerCommentAPIView(APIView):
    def get_object(self, pk):
        try:
            return AnswerComment.objects.get(pk=pk)
        except AnswerComment.DoesNotExist:
            raise Http404

    # CRUD 중 R
<<<<<<< HEAD
    def get(self, request, pk, format=None):
        comment = self.get_object(pk)
=======
    def get(self, request, pk, comment_pk, reply_pk, format=None):
        comment = self.get_object(reply_pk)
>>>>>>> develop
        serializer = AnswerCommentSerializer(comment)
        return Response(serializer.data)

    # CRUD 중 U
<<<<<<< HEAD
    def put(self, request, pk, format=None):
        comment = self.get_object(pk)
        # print(request.user.id)
        if comment.author_id.id == request.user.id:  # 작성자가 같을때만 수정 가능
            serializer = AnswerCommentSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "자신의 댓글이 아닙니다."}, status=status.HTTP_403_FORBIDDEN
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    ## 자기거만 삭제
    # CRUD 중 D
    def delete(self, request, pk, format=None):
        comment = self.get_object(pk)
        if comment.author_id.id == request.user.id:  # 작성자가 같을때만 삭제 가능
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"message": "자신의 댓글이 아닙니다."}, status=status.HTTP_403_FORBIDDEN
            )


class AnswerCommentListAPIView(APIView):  ## auther_id 도 나와야함
    def get(self, request, pk, comment_pk):  # 모든 게시물
        comments = AnswerComment.objects.all()
=======
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
>>>>>>> develop
        serializer = AnswerCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk, comment_pk):
<<<<<<< HEAD
        serializer = AnswerCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
=======
        if request.user.is_authenticated:
            serializer = AnswerCommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author_id_id=request.user.id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
>>>>>>> develop
