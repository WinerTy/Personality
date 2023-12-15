from .models import Post
from django import forms
from django.forms import TextInput, Textarea, Select


# Форма создания поста
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title','text', 'type']

        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заголовок',
            }),
            "text": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Содержание поста',
            }),
            "type": Select(attrs={
                'class': 'form-control',
                'placeholder': 'Тип поста',
            }),
        }

    def save(self, user, commit=True):
        post = super().save(commit=False)
        post.author = user
        if commit:
            post.save()
        return post