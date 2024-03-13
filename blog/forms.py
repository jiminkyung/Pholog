from django import forms
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
from .models import Post, Image, Comment, Category


class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": "태그를 '#'로 구분하여 입력하세요. 예: #Python #Django #Web",
            }
        ),
    )

    class Meta:
        model = Post
        fields = ["title", "content", "categories"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "input", "placeholder": "제목"}),
            "content": forms.Textarea(
                attrs={"class": "textarea", "placeholder": "내용을 입력해주세요."}
            ),
            "categories": forms.SelectMultiple(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields["categories"].required = False
        if self.instance.pk:
            self.fields["tags"].initial = " ".join(f"#{tag.name}" for tag in self.instance.tags.all())

        if user is not None:
            self.fields["categories"].queryset = Category.objects.filter(author=user)


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["image"]

ImageFormSet = inlineformset_factory(
    Post, Image, form=ImageForm, fields=["image"], extra=5, can_delete=True
)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "댓글을 입력해주세요.", "rows": 3,}
            ),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data["name"]
        if Category.objects.filter(name=name).exists():
            raise ValidationError(f"'{name}'라는 이름의 카테고리는 이미 존재합니다.")
        return name