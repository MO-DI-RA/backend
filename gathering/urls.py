from django.urls import path
from .views import *

app_name = "main"

urlpatterns = [
    path("posts/", ListAPIView.as_view()),
    path("posts/<int:pk>", PostAPIView.as_view()),
    path("posts/<int:pk>/comments/", CommentListAPIView.as_view()),
    path("posts/<int:pk>/comments/<int:comment_pk>/", CommentAPIView.as_view()),
    path("posts/search/", PostViewSet.as_view()),
]
