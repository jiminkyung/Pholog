from django import forms
from django.forms import inlineformset_factory
from .models import Post, Image, Comment


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
        fields = ["title", "content",]
        labels = {"title": "", "content": ""}
        widgets = {
            "title": forms.TextInput(attrs={"class": "input", "placeholder": "제목"}),
            "content": forms.Textarea(
                attrs={"class": "textarea", "placeholder": "내용을 입력해주세요."}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['tags'].initial = ' '.join(f'#{tag.name}' for tag in self.instance.tags.all())


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
        labels = {"content": ""}
        widgets = {
            "content": forms.Textarea(
                attrs={"class": "textarea", "placeholder": "댓글을 입력해주세요."}
            ),
        }