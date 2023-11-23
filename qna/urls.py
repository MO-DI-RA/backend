from django.urls import path
from .views import *


urlpatterns = [
    path("posts/", ListAPIView.as_view()),
    path("posts/<int:pk>/", PostAPIView.as_view()),
    path("posts/<int:pk>/comments/", AnswerListAPIView.as_view()),
    path("posts/<int:pk>/comments/<int:comment_pk>/", AnswerAPIView.as_view()),
    path(
        "posts/<int:pk>/comments/<int:comment_pk>/reply/",
        AnswerCommentListAPIView.as_view(),
    ),
    path(
        "posts/<int:pk>/comments/<int:comment_pk>/reply/<int:reply_pk>/",
        AnswerCommentAPIView.as_view(),
    ),
    path("posts/<int:pk>/toggle/", PostToggleStatus.as_view()),
    path("posts/search/", PostViewSet.as_view()),
    path("posts/<int:post_id>/interest/", InterestedPost.as_view()),
    path("posts/interest/", UserInterestListAPI.as_view()),
    path("posts/myposts/", UserPostAPIView.as_view()),
]
