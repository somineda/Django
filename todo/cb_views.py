from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from todo.models import Todo, Comment
from todo.forms import TodoForm, TodoUpdateForm, CommentForm


# -------------------
# ✅ Todo Views
# -------------------

class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    template_name = 'todo/todo_list.html'   # ✅
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
    template_name = 'todo/todo_info.html'   # ✅

    def get_object(self, queryset=None):
        obj = super().get_object()
        if self.request.user != obj.user and not self.request.user.is_superuser:
            raise Http404("해당 To Do를 볼 수 없습니다.")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        todo = self.get_object()
        comments = todo.comments.all().order_by('-created_at')

        paginator = Paginator(comments, 5)
        page = self.request.GET.get('page')
        page_obj = paginator.get_page(page)

        context['todo'] = todo.__dict__
        context['form'] = CommentForm()
        context['page_obj'] = page_obj
        return context


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    form_class = TodoForm
    template_name = 'todo/todo_create.html'   # ✅

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('cbv_todo_info', kwargs={'pk': self.object.pk})


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    form_class = TodoUpdateForm
    template_name = 'todo/todo_update.html'   # ✅

    def get_object(self, queryset=None):
        obj = super().get_object()
        if self.request.user != obj.user and not self.request.user.is_superuser:
            raise Http404("해당 To Do를 수정할 권한이 없습니다.")
        return obj

    def get_success_url(self):
        return reverse('cbv_todo_info', kwargs={'pk': self.object.pk})


class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo
    template_name = 'todo/todo_confirm_delete.html'   # ❗해당 파일은 templates 폴더에 없는 것 같아요

    def get_object(self, queryset=None):
        obj = super().get_object()
        if self.request.user != obj.user and not self.request.user.is_superuser:
            raise Http404("해당 To Do를 삭제할 권한이 없습니다.")
        return obj

    def get_success_url(self):
        return reverse_lazy('cbv_todo_list')


# -------------------
# ✅ Comment Views
# -------------------

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'todo_id'

    def form_valid(self, form):
        todo = get_object_or_404(Todo, id=self.kwargs['todo_id'])
        comment = form.save(commit=False)
        comment.todo = todo
        comment.user = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('cbv_todo_info', kwargs={'pk': self.kwargs['todo_id']})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'todo/comment_form.html'   # ✅ 템플릿이 필요함 (스크린샷엔 아직 없음)

    def get_object(self, queryset=None):
        comment = super().get_object(queryset)
        if self.request.user != comment.user and not self.request.user.is_superuser:
            raise Http404("해당 댓글을 수정할 권한이 없습니다.")
        return comment

    def get_success_url(self):
        return reverse('cbv_todo_info', kwargs={'pk': self.object.todo.id})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'todo/comment_confirm_delete.html'  # ✅ 템플릿이 필요함 (스크린샷엔 아직 없음)

    def get_object(self, queryset=None):
        comment = super().get_object(queryset)
        if self.request.user != comment.user and not self.request.user.is_superuser:
            raise Http404("해당 댓글을 삭제할 권한이 없습니다.")
        return comment

    def get_success_url(self):
        return reverse('cbv_todo_info', kwargs={'pk': self.object.todo.id})
