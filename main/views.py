from django.shortcuts import render
from blog.models import Post

def index(request):
    posts = Post.objects.all().prefetch_related("images")
    context = {"posts": posts}
    return render(request, "main/index.html", context)