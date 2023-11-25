from .models import GatheringPost, Comment, GatheringLike
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
        if request.user.is_authenticated:
            print(request.user.id)
            serializer = PostListSerializer(data=request.data)
            print(request.data)
            if serializer.is_valid():
                serializer.save(author_id_id=request.user.id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class UserPostAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            user_id = request.user.id
            print(user_id)
            posts = GatheringPost.objects.filter(author_id=user_id)
            print(posts)
            serializer = PostListSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


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
        if request.user.is_authenticated:
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
        if request.user.is_authenticated:
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
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    # CRUD 중 D
    def delete(self, request, pk, comment_pk, format=None):
        if request.user.is_authenticated:
            comment = self.get_object(comment_pk)
            if comment.author_id.id == request.user.id:  # 작성자가 같을때만 삭제 가능
                comment.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {"message": "자신의 댓글이 아닙니다."}, status=status.HTTP_403_FORBIDDEN
                )
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class LikeAPIView(APIView):
    def post(self, request, post_id):
        if request.user.is_authenticated:
            user = request.user
            post = GatheringPost.objects.get(id=post_id)  # 있는지 없는지 처리 해야함
            print(post)
            print(user)
            # 이미 좋아요가 눌렸는지 확인
            like, created = GatheringLike.objects.get_or_create(user=user, post=post)
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


class UserInterestListAPI(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            likes = GatheringLike.objects.filter(user=user)
            liked_posts = GatheringPost.objects.filter(
                id__in=likes.values_list("post", flat=True)
            )
            serializer = PostListSerializer(liked_posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            Response(status=status.HTTP_401_UNAUTHORIZED)


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
        if request.user.is_authenticated:
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author_id_id=request.user.id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)