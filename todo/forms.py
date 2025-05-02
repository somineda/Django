from django import forms
from todo.models import Todo, Comment
from django_summernote.widgets import SummernoteWidget


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title", "description", "start_date", "end_date"]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': SummernoteWidget(),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class TodoUpdateForm(forms.ModelForm):
    is_completed = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Todo
        fields = ["title", "description", "start_date", "end_date", "is_completed", "completed_image"]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': SummernoteWidget(),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'completed_image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']
        labels = {
            'message': '내용',
        }
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 3,
                'cols': 40,
                'class': 'form-control',
                'placeholder': '댓글을 입력하세요...',
            })
        }
