from django import forms

from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(
        max_length=25,
        label='Ваше имя',
    )
    email = forms.EmailField(
        label='Ваш email'
    )
    to = forms.EmailField(
        label='Email получателя'
    )
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea,
        label='Комментарий для получателя'
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'text')
        help_texts = {
            'name': None,
            'email': None,
            'text': None
        }


class SearchForm(forms.Form):
    query = forms.CharField(
        label='Запрос',
    )
