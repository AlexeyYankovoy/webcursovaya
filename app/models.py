"""
Definition of models.
"""

from django.db import models
from django.contrib import admin
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User

class Blog(models.Model):
    title=models.CharField('Название', max_length=50, unique_for_date='date')
    description=models.CharField('Краткое содержание', max_length=200)
    content=models.TextField('Полное содержание')
    date=models.DateTimeField('Дата публикации', default=datetime.now(), db_index=True)
    author=models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Автор статьи')
    image=models.FileField(default='temp.jpg', verbose_name='Путь к картинке')
    def get_absolute_url(self):
        return reverse("newspost", args=[str(self.id)])
    def __str__(self):
        return self.title

    class Meta:
        db_table='Posts'
        ordering=["-date"]
        verbose_name='Статья'
        verbose_name_plural='Статьи'
admin.site.register(Blog)

class Comment(models.Model):
    text=models.TextField('Текст комментария')
    date=models.DateTimeField(default=datetime.now(), db_index=True, verbose_name='Дата комментария')
    author=models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария')
    post=models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='Статья комментария')
    def __str__(self):
        return 'Комментарий %d от пользователя %s к статье %s' % (self.id, self.author, self.post)
    class Meta:
        db_table='Comment'
        ordering=['-date']
        verbose_name='Комментарии к статье'
        verbose_name_plural='Комментарии к статьям'
admin.site.register(Comment)
# Create your models here.
