# config/urls.py

from django.contrib import admin
from django.urls import path, include
from users import views as users_views
from todo.views import todo_list, todo_info, todo_update, todo_delete, todo_create

urlpatterns = [
    path('admin/', admin.site.urls),

    # FBV
    path('todo/', todo_list, name='todo_list'),
    path('todo/<int:todo_id>/', todo_info, name='todo_info'),
    path('todo/<int:todo_id>/update/', todo_update, name='todo_update'),
    path('todo/<int:todo_id>/delete/', todo_delete, name='todo_delete'),
    path('todo/create/', todo_create, name='todo_create'),

    # Auth
    path('accounts/login/', users_views.login, name='login'),
    path('accounts/signup/', users_views.sign_up, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),

    # ✅ CBV URL include
    path('cbv/', include('todo.urls')),
]
