from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as django_login

def sign_up(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(settings.LOGIN_URL)  # 회원가입 성공하면 로그인 페이지로

    return render(request, 'registration/signup.html', {'form': form})

def login(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        django_login(request, form.get_user())
        return redirect(settings.LOGIN_REDIRECT_URL)  # 로그인 성공하면 todo 페이지로

    return render(request, 'registration/login.html', {'form': form})

