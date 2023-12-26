"""
Definition of forms.
"""

from django import forms
from django.db import models
from .models import Comment, Blog, Product
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

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

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'category', 'image', 'description', 'technical_specifications', 'price')
        labels = {
            'name': "Название товара",
            'category': "Категория товара",
            'image': "Изображение",
            'description': "Описание",
            'technical_specifications': "Технические характеристики",           
            'price': "Цена",            
        }