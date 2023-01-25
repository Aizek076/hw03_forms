from .models import Post
from django.forms import ModelForm
from django import forms


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')

    def clean_text(self):
        data = self.cleaned_data['text']
        if len(data) == 0:
            raise forms.ValidationError('пустая форма')
        return data