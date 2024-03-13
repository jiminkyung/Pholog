from django.contrib import admin
from .models import Post, Comment, Image, Tag, Category

class CommentAdmin(admin.ModelAdmin):
    list_display = ["author", "message"]
    search_fields = ["author__username", "message"]

admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Category)