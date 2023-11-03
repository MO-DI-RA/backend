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


class ListAPIView(APIView):  ## auther_id 도 나와야함
    def get(self, request):  # 모든 게시물
        posts = GatheringPost.objects.all()
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PostListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        return Response(serializer.data)

    # CRUD 중 U
    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostDetailSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # CRUD 중 D
    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
