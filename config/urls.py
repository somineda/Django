"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import Http404
from django.shortcuts import render
from fake_db import users

# 내부 데이터
_db = {user["id"]: user for user in users}

# 뷰 함수 1: 유저 목록
def user_list(request):
    names = [{'id': user["id"], 'name': user["name"]} for user in users]
    return render(request, 'user_list.html', {'data': names})

# 뷰 함수 2: 유저 상세
def user_info(request, user_id):
    user = _db.get(user_id)
    if not user:
        raise Http404('User not found')
    return render(request, 'user_info.html', {'data': user})

# URL 패턴
urlpatterns = [
    path('users/', user_list, name='user_list'),
    path('users/<int:user_id>/', user_info, name='user_info'),
    path('admin/', admin.site.urls),
]

