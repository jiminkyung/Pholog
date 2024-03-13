from django.urls import path
from . import views

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("all/", views.all_post_list, name="all_post_list"),
    path("create/", views.post_create, name="post_create"),
    path("<int:pk>/", views.post_detail, name="post_detail"),
    path("<int:pk>/update/", views.post_update, name="post_update"),
    path("<int:pk>/delete/", views.post_delete, name="post_delete"),
    path("<int:pk>/comment/", views.comment_create, name="comment_create"),
    path("comment/<int:pk>/update/", views.comment_update, name="comment_update"),
    path("comment/<int:pk>/delete/", views.comment_delete, name="comment_delete"),
    path("category/", views.category_list, name="category_list"),
    path("category/create/", views.category_create, name="category_create"),
    path("category/<int:pk>/update/", views.category_update, name="category_update"),
    path("category/<int:pk>/delete/", views.category_delete, name="category_delete"),
    path("tag/<str:tag_name>/", views.tag_list, name="tag_list"),
]