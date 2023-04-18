#forms는 컨벤션에 걸리지 않으니 이름은 맘대로

from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment #이 모델 폼의 근본적인 정보'
        fields = ['content',]