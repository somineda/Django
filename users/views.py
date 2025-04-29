from django.shortcuts import render
from fake_db import users

def user_list(request):
    names = [user["name"] for user in users]
    return render(request, "user_list.html", {"names": names})

def user_info(request, user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    return render(request, "user_info.html", {"user": user})

# Create your views here.
