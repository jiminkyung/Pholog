# import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


# 카테고리 모델
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "카테고리"
        verbose_name_plural = "카테고리 그룹"

    def __str__(self):
        return self.name


# 태그 모델
class Tag(models.Model):
    name = models.CharField(max_length=40, unique=True)

    class Meta:
        verbose_name = "태그"
        verbose_name_plural = "태그 그룹"

    def __str__(self):
        return self.name


# 게시글 모델
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    categories = models.ManyToManyField(Category, blank=True, related_name="post_categories")
    tags = models.ManyToManyField(Tag, blank=True, related_name="post_tags")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "포스트"
        verbose_name_plural = "포스트 그룹"
        ordering = ["-created_at"]


    def __str__(self):
        return self.title


class Image(models.Model):
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="blog/%Y/%m/%d/")

    class Meta:
        verbose_name = "이미지"
        verbose_name_plural = "이미지 그룹"

    def __str__(self):
        return f"{self.post.title} - Image {self.id}"


# 댓글 모델
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "댓글"
        verbose_name_plural = "댓글 그룹"

    def __str__(self):
        return self.content