from django import forms
from todo.models import Todo


# 생성(Create) 용 폼 - 완료 여부는 제외
class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title", "description", "start_date", "end_date"]


# 수정(Update) 용 폼 - 완료 여부(is_completed) 포함
class TodoUpdateForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title", "description", "start_date", "end_date", "is_completed"]
