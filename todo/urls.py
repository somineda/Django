# todo/urls.py

from django.urls import path
from .cb_views import (
    TodoListView, TodoDetailView, TodoCreateView,
    TodoUpdateView, TodoDeleteView,
)

urlpatterns = [
    path('', TodoListView.as_view(), name='cbv_todo_list'),
    path('create/', TodoCreateView.as_view(), name='cbv_todo_create'),
    path('<int:pk>/', TodoDetailView.as_view(), name='cbv_todo_info'),
    path('<int:pk>/update/', TodoUpdateView.as_view(), name='cbv_todo_update'),
    path('<int:pk>/delete/', TodoDeleteView.as_view(), name='cbv_todo_delete'),
]
