from .models import QnAPost, Answer, AnswerComment
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


class ListAPIView(APIView):  ## auther_id 도 나와야함
    def get(self, request):  # 모든 게시물
        posts = QnAPost.objects.all()
        serializer = QnAListSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        print(request.user.id)
        serializer = QnAListSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save(author_id_id=request.user.id)  # 이런식으로 바꿔줘
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class PostToggleStatus(APIView):
    def get_object(self, pk):
        try:
            return QnAPost.objects.get(pk=pk)
        except QnAPost.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        if post.author_id.id == request.user.id:
            post.status = not post.status
            post.save()
            return Response({"message": "게시물 상태가 토글되었습니다."}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "자신의 게시물이 아닙니다."}, status=status.HTTP_403_FORBIDDEN
            )


class AnswerAPIView(APIView):
    def get_object(self, pk):
        try:
            return Answer.objects.get(pk=pk)
        except Answer.DoesNotExist:
            raise Http404

    # CRUD 중 R
    def get(self, request, pk, format=None):
        comment = self.get_object(pk)
        serializer = AnswerSerializer(comment)
        return Response(serializer.data)

    # CRUD 중 U
    def put(self, request, pk, format=None):
        comment = self.get_object(pk)
        # print(request.user.id)
        if comment.author_id.id == request.user.id:  # 작성자가 같을때만 수정 가능
            serializer = AnswerSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "자신의 답변이 아닙니다."}, status=status.HTTP_403_FORBIDDEN
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


class AnswerListAPIView(APIView):  ## auther_id 도 나와야함
    def get(self, request):  # 모든 게시물
        comments = Answer.objects.all()
        serializer = AnswerSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnswerCommentAPIView(APIView):
    def get_object(self, pk):
        try:
            return AnswerComment.objects.get(pk=pk)
        except AnswerComment.DoesNotExist:
            raise Http404

    # CRUD 중 R
    def get(self, request, pk, format=None):
        comment = self.get_object(pk)
        serializer = AnswerCommentSerializer(comment)
        return Response(serializer.data)

    # CRUD 중 U
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
        serializer = AnswerCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk, comment_pk):
        serializer = AnswerCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
