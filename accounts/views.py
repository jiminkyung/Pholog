from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views.generic import CreateView


signup = CreateView.as_view(
    form_class = UserCreationForm,
    template_name = "accounts/form.html",
    success_url = "/accounts/login/"
)


login = LoginView.as_view(
    template_name = "accounts/form.html",
)


logout = LogoutView.as_view(
    next_page = "/accounts/login/"
)


@login_required
def profile(request):
    return render(request, "accounts/profile.html")