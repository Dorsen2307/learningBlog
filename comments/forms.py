from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-name', 'placeholder': 'Ваше имя'}),
            'content': forms.Textarea(attrs={'class': 'form-comment', 'placeholder': 'Ваш комментарий'})
        }