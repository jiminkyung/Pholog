from django.db import models
from django.contrib.auth.models import User

# 카테고리 모델
class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# 태그 모델
class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# 게시글 모델
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    categories = models.ManyToManyField(Category, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    thumbnail = models.ForeignKey('Image', related_name='thumbnails', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# 이미지 모델 - 날짜별로 이미지 저장
class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="blog/images/%Y/%m/%d/", blank=True)

    def __str__(self):
        return self.image.name

# 댓글 모델
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content