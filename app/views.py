"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.forms import UserCreationForm
from .forms import FeedbackForm
from django.db import models
from .models import Blog
from .models import Comment
from .forms import CommentForm
from .forms import BlogForm

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная страница',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Страница с нашими контактами',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Сведения о нас',
            'year':datetime.now().year,
        }
    )

def links(request):
    """Renders the links page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Ссылки',
            'message':'Полезные ресурсы',
            'year':datetime.now().year,
        }
    )

def registration(request):
    """Renders the registration page."""
    assert isinstance(request, HttpRequest)
    if request.method == "POST": # после отправки формы
        regform=UserCreationForm(request.POST)
        if regform.is_valid(): # валидация полей формы
            reg_f=regform.save(commit=False) # не сохраняем автоматически данные формы
            reg_f.is_staff=False # запрещен вход в администативный раздел
            reg_f.is_active=True # активный пользователь
            reg_f.is_superuser=False # не суперпользователь
            reg_f.date_joined=datetime.now() # дата регистрации
            reg_f.last_login=datetime.now() # дата последней авторизации
            reg_f.save() # сохраняем изменения после изменения данных
            return redirect('home') # возвращаем на главную страницу после регистрации
    else:
        regform=UserCreationForm() # создание объекта формы для ввода данных нового пользователя
    return render(
        request,
        'app/registration.html',
        {
            'title':'Регистация',
            'regform':regform, # передача формы в шаблон веб-страницы
            'year':datetime.now().year,
        }
    )

def feedback(request):
    """Renders the links page."""
    assert isinstance(request, HttpRequest)
    data=None
    like={'1': 'Да', '2': 'Нет'}
    if request.method=='POST':
        form=FeedbackForm(request.POST)
        if form.is_valid():
            data=dict()
            data['name']=form.cleaned_data['name']
            data['email']=form.cleaned_data['email']
            data['like']=like[form.cleaned_data['like']]
            data['msg']=form.cleaned_data['msg']
            form=None
    else:
        form=FeedbackForm()
    return render(
        request,
        'app/feedback.html',
        {
            'title':'Оставить отзыв',
            'form':form,
            'data':data,
            'year':datetime.now().year,
        }
    )

def news(request):
    """Renders the news page."""
    posts=Blog.objects.all()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/news.html',
        {
            'title':'Новости',
            'posts': posts,
            'year':datetime.now().year,
        }
    )

def newspost(request, parametr):
    """Renders the newspost page."""
    assert isinstance(request, HttpRequest)
    post_1=Blog.objects.get(id=parametr)
    comments=Comment.objects.filter(post=parametr)

    if request.method=="POST":
        form=CommentForm(request.POST)
        if form.is_valid():
            comment_f=form.save(commit=False)
            comment_f.author=request.user
            comment_f.date=datetime.now()
            comment_f.post=Blog.objects.get(id=parametr)
            comment_f.save()
            return redirect('newspost', parametr=post_1.id)
    else:
        form=CommentForm()
    return render(
        request,
        'app/newspost.html',
        {
            'post_1': post_1,
            'comments':comments,
            'form':form,
            'title': post_1.title,
            'year':datetime.now().year,
        }
    )

def newpost(request):
    """Renders the newpost page."""
    assert isinstance(request, HttpRequest)
    if request.method=="POST":
        blogform=BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f=blogform.save(commit=False)
            blog_f.date=datetime.now()
            blog_f.author=request.user
            blog_f.save()
            return redirect('news')
    else:
        blogform=BlogForm()
    return render(
        request,
        'app/newpost.html',
        {
            'blogform':blogform,
            'title': 'Добавить статью',
            'year':datetime.now().year,
        }
    )

def video(request):
    """Renders the video page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/video.html',
        {
            'title':'Видео',
            'year':datetime.now().year,
        }
    )