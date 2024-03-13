from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment, Tag, Category
from .forms import PostForm, ImageFormSet, CommentForm, CategoryForm
import logging


# 전체 게시글 목록
class AllPostListView(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "posts/all_post_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get("q")
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) | Q(content__icontains=q)
            ).distinct()
        return queryset

# 유저 게시글 목록
class PostListView(LoginRequiredMixin, AllPostListView):
    template_name = "posts/post_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(author=self.request.user)
        return queryset


# 게시글 상세페이지
class PostDetailView(FormMixin, DetailView):
    model = Post
    form_class = CommentForm
    template_name = "posts/post_detail.html"

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context["comment_form"] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.get_object()
        comment.author = self.request.user
        comment.save()
        return super(PostDetailView, self).form_valid(form)


# 태그 처리
def process_tags(tags_str):
    tag_names = tags_str.split("#")
    tag_names = [name.strip() for name in tag_names if name.strip()]
    tags = []
    for tag_name in tag_names:
        tag, created = Tag.objects.get_or_create(name=tag_name)
        tags.append(tag)
    return tags


# 게시글 생성
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"

    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["image_formset"] = ImageFormSet(self.request.POST, self.request.FILES)
        else:
            context["image_formset"] = ImageFormSet()
        return context
    
    def get_form_kwargs(self):
        kwargs = super(PostCreateView, self).get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context["image_formset"]
        if image_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.author = self.request.user
            self.object.save()
            form.save_m2m()
        
            # 태그 처리
            tags_str = form.cleaned_data.get("tags", "")
            tags = process_tags(tags_str)
            self.object.tags.set(tags)

            image_formset.instance = self.object
            image_formset.save()
            return redirect("post_list")
        else:
            return self.render_to_response(self.get_context_data(form=form))


# 게시글 수정
logger = logging.getLogger(__name__)

class PostUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"

    def get_context_data(self, **kwargs):
        context = super(PostUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["image_formset"] = ImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context["image_formset"] = ImageFormSet(instance=self.object)
        if "image_formset_errors" not in context:
            context["image_formset_errors"] = None
        return context
    
    def get_form_kwargs(self):
        kwargs = super(PostCreateView, self).get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context["image_formset"]
        if image_formset.is_valid():
            self.object = form.save()
            try:
                image_formset.instance = self.object
                image_formset.save()
            except ValueError as e:
                # 예외 발생 시 로그에 기록, 사용자에게 메시지 전달.
                logger.error(f"Error saving image formset: {e}")
                form.add_error(None, "이미지를 저장하는 동안 오류가 발생했습니다.")
                return self.render_to_response(self.get_context_data(form=form))

            # 태그 처리
            tags_str = form.cleaned_data.get("tags", "")
            tags = process_tags(tags_str)
            self.object.tags.set(tags)

            return redirect("post_list")
        else:
            logger.error(f"ImageFormSet validation failed: {image_formset.errors}")
            return super().form_invalid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# 게시글 삭제
class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("post_list")
    template_name = "posts/post_confirm_delete.html"

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# 댓글 생성
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs["pk"])
        form.save()
        return redirect("post_detail", pk=form.instance.post.pk)


# 댓글 수정
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "comments/comment_form.html"

    def form_valid(self, form):
        form.save()
        return redirect("post_detail", pk=self.object.post.pk)

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


# 댓글 삭제
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "comments/comment_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"pk": self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


# 카테고리 목록
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "categories/category_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        return Category.objects.filter(author=self.request.user)


# 카테고리 생성 뷰
class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "categories/category_form.html"
    success_url = reverse_lazy("category_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_edit"] = False
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# 카테고리 수정 뷰
class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "categories/category_form.html"
    success_url = reverse_lazy("category_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_edit"] = True
        return context


# 카테고리 삭제 뷰
class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy("category_list")
    template_name = "categories/category_confirm_delete.html"


# 태그 뷰
def tag_list(request, tag_name):
    posts = Post.objects.filter(tags__name=tag_name)
    posts_counted = posts.count()
    context = {"posts": posts, "tag_name": tag_name, "posts_counted": posts_counted}
    return render(request, "posts/tag_list.html", context)


# URL 경로
all_post_list = AllPostListView.as_view()
post_list = PostListView.as_view()
post_detail = PostDetailView.as_view()
post_create = PostCreateView.as_view()
post_update = PostUpdateView.as_view()
post_delete = PostDeleteView.as_view()

comment_create = CommentCreateView.as_view()
comment_update = CommentUpdateView.as_view()
comment_delete = CommentDeleteView.as_view()

category_list = CategoryListView.as_view()
category_create = CategoryCreateView.as_view()
category_update = CategoryUpdateView.as_view()
category_delete = CategoryDeleteView.as_view()