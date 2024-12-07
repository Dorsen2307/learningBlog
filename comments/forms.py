from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-name', 'placeholder': 'Ваше имя'}),
            'content': forms.Textarea(attrs={'class': 'form-comment', 'placeholder': 'Ваш комментарий'})
        }

    def __init__(self, *args, **kwargs):
        user_authenticated = kwargs.pop('user_authenticated', False)
        super(CommentForm, self).__init__(*args, **kwargs)

        if user_authenticated:
            self.fields.pop('name', None)
        else:
            self.fields['name'].required = True
