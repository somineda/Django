from django.contrib import admin
from todo.models import Todo, Comment
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Todo)
class TodoAdmin(SummernoteModelAdmin):
    list_display = ('title', 'description', 'is_completed', 'start_date', 'end_date')
    list_filter = ('is_completed',)
    search_fields = ('title',)
    ordering = ('start_date',)
    summernote_fields = ('description',)

    fieldsets = (
        ('Todo Info', {
            'fields': ('user', 'title', 'description', 'is_completed')
        }),
        ('Date & Image', {
            'fields': ('start_date', 'end_date', 'completed_image')
        }),
    )
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('todo', 'user', 'message', 'created_at')
    search_fields = ('message',)
    ordering = ('-created_at',)
