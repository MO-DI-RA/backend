from django.urls import path
from .views import *

app_name = "main"

urlpatterns = [
    path("posts/", ListAPIView.as_view()),
    path("posts/<int:pk>/", PostAPIView.as_view()),
    path("posts/<int:pk>/comments/", CommentListAPIView.as_view()),
    path("posts/<int:pk>/comments/<int:comment_pk>/", CommentAPIView.as_view()),
    path("posts/search", PostViewSet.as_view()),
    path("posts/myposts/", UserPostAPIView.as_view()),
    path("posts/<int:post_id>/like/", LikeAPIView.as_view()),
    path("posts/unlike/", LikeDeleteView.as_view()),
    path("posts/interest/", UserInterestListAPI.as_view()),
    # path("posts/<int:post_id>/status/", LikeStatusView.as_view()),
]
