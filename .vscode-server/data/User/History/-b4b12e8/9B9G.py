from django.urls import path
from .views import MovieList, movie_detail, actor_list, actor_detail, review_list

# 여기를 수정해 주세요.
urlpatterns = [
    path('movies', MovieList.as_view()),
    path('actors', ActorList.as_view()),
    path('movies/<int:pk>', movie_detail),
    path('actors/<int:pk>', actor_detail),
    path('movies/<int:pk>/reviews', review_list),
]