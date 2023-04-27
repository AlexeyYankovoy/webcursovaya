"""
Definition of forms.
"""

from django import forms
from django.db import models
from .models import Comment
from .models import Blog
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))

class FeedbackForm(forms.Form):
    name=forms.CharField(label='Ваше имя', min_length=2, max_length=30)
    email=forms.EmailField(label='Ваш e-mail', min_length=7)
    like = forms.ChoiceField(label='Нравится ли вам наш сайт?', choices=[('1', 'Да'),('2', 'Нет')], widget=forms.RadioSelect, initial=1)
    msg=forms.CharField(label='Ваши пожелания и идеи', widget=forms.Textarea(attrs={'rows':8, 'cols':40}))

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('text',)
        labels={'text':""}

class BlogForm(forms.ModelForm):
    class Meta:
        model=Blog
        fields=('title', 'description', 'content', 'image')
        labels={'title':"Название", 'description':"Краткое содержание", 'content':"Полное содержание", 'image':"Картинка"}
