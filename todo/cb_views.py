# todo/cb_views.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.http import Http404
from django.urls import reverse_lazy, reverse
from todo.models import Todo

class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    template_name = 'todo/todo_list.html'
    paginate_by = 10
    ordering = ['-created_at']
    context_object_name = 'page_obj'

    def get_queryset(self):
        qs = Todo.objects.all() if self.request.user.is_superuser else Todo.objects.filter(user=self.request.user)
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        return qs

class TodoDetailView(LoginRequiredMixin, DetailView):
    model = Todo
    template_name = 'todo/todo_info.html'

    def get_object(self, queryset=None):
        obj = super().get_object()
        if self.request.user != obj.user and not self.request.user.is_superuser:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todo'] = self.get_object().__dict__
        return context

class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    fields = ['title', 'description', 'start_date', 'end_date']
    template_name = 'todo/todo_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('cbv_todo_info', kwargs={'pk': self.object.pk})

class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    fields = ['title', 'description', 'start_date', 'end_date', 'is_completed']
    template_name = 'todo/todo_update.html'

    def get_object(self, queryset=None):
        obj = super().get_object()
        if self.request.user != obj.user and not self.request.user.is_superuser:
            raise Http404
        return obj

    def get_success_url(self):
        return reverse('cbv_todo_info', kwargs={'pk': self.object.pk})

class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo
    template_name = 'todo/todo_confirm_delete.html'

    def get_object(self, queryset=None):
        obj = super().get_object()
        if self.request.user != obj.user and not self.request.user.is_superuser:
            raise Http404
        return obj

    def get_success_url(self):
        return reverse_lazy('cbv_todo_list')
