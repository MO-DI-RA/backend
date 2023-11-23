from .models import GatheringPost, Comment
from .serializers import (
    PostDetailSerializer,
    PostListSerializer,
    CommentSerializer,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from rest_framework import generics
from rest_framework.filters import SearchFilter


class ListAPIView(APIView):  ## auther_id 도 나와야함
    def get(self, request):  # 모든 게시물
        posts = GatheringPost.objects.all()
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        print(request.user.id)
        serializer = PostListSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save(author_id_id=request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPostAPIView(APIView):
    def get(self, request):
        user_id = request.user.id
        print(user_id)
        posts = GatheringPost.objects.filter(author_id=user_id)
        print(posts)
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# post
class PostAPIView(APIView):
    def get_object(self, pk):
        try:
            return GatheringPost.objects.get(pk=pk)
        except GatheringPost.DoesNotExist:
            raise Http404

    # CRUD 중 R
    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostDetailSerializer(post)
        return Response(data=serializer.data)

    # CRUD 중 U
    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        # print(request.user.id)
        if post.author_id.id == request.user.id:  # 작성자가 같을때만 수정 가능
            serializer = PostDetailSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save(author_id_id=request.user.id)
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


class CommentAPIView(APIView):
    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404

    # CRUD 중 R
    def get(self, request, pk, comment_pk, format=None):
        comment = self.get_object(comment_pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    # CRUD 중 U
    def put(self, request, pk, comment_pk, format=None):
        comment = self.get_object(comment_pk)
        # print(request.user.id)
        if comment.author_id.id == request.user.id:  # 작성자가 같을때만 수정 가능
            serializer = CommentSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save(author_id_id=request.user.id)
                return Response(serializer.data, status=status.HTTP_200_OK)  #
        else:
            return Response(
                {"message": "자신의 댓글이 아닙니다."}, status=status.HTTP_403_FORBIDDEN
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


class PostViewSet(generics.ListAPIView):
    queryset = GatheringPost.objects.all()
    serializer_class = PostDetailSerializer
    filter_backends = [SearchFilter]
    search_fields = ["title"]


class CommentListAPIView(APIView):  ## auther_id 도 나와야함
    def get(self, request, pk):  # 모든 게시물
        comments = Comment.objects.all().filter(post_id=pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author_id_id=request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
