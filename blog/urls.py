from django.urls import path
from . import views

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("create/", views.post_create, name="post_create"),
    path("<int:pk>/", views.post_detail, name="post_detail"),
    path("<int:pk>/update/", views.post_update, name="post_update"),
    path("<int:pk>/delete/", views.post_delete, name="post_delete"),
    path("<int:pk>/comment/", views.comment_create, name="comment_create"),
    path("comment/<int:pk>/update/", views.comment_update, name="comment_update"),
    path("comment/<int:pk>/delete/", views.comment_delete, name="comment_delete"),
]