from django.urls import path, include
from . import views

urlpatterns = [
    path('diary/', views.page_list),
    # path('diafy/info/', views.info),
    # path('diary/write/', views.page_create),
    # path('diary/page/<int:page_id>/', views.page_detail),
    # path('diary/page/<int:page_id>/edit/', views.page_update),
    # path('diary/page/<int:page_id>/delete/', views.page_delete),
]