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
    date=models.DateTimeField('Дата публикации', default=datetime.now, db_index=True)
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
    date=models.DateTimeField(default=datetime.now, db_index=True, verbose_name='Дата комментария')
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

class Category(models.Model):
    name=models.CharField(max_length=255, verbose_name='Название')
    def __str__(self):
        return self.name
    class Meta:
        db_table='Category'        
        verbose_name='Категория'
        verbose_name_plural='Категории'
admin.site.register(Category)

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория товара')   
    image = models.ImageField(upload_to='Product_images/', null=True, blank=True, verbose_name='Изображение')
    description = models.TextField('Описание')
    technical_specifications = models.TextField('Технические характеристики')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Цена')    
    def get_technical_specifications_as_paragraphs(self):
        return [f'<p>{paragraph}</p>' for paragraph in self.technical_specifications.split('\n') if paragraph.strip()]
    def __str__(self):
        return self.name
    class Meta:
        db_table='Product'        
        verbose_name='Товар'
        verbose_name_plural='Товары'
admin.site.register(Product)

class OrderStatus(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название статуса")   

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Статус заказа"
        verbose_name_plural = "Статусы заказов"

admin.site.register(OrderStatus)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая сумма", default=0.00)
    is_sent = models.BooleanField(default=False, verbose_name="Заказ отправлен")
    status = models.ForeignKey(OrderStatus, default=4, on_delete=models.SET_DEFAULT, verbose_name="Статус")

    def update_total_amount(self):
        total_amount = self.order_items.aggregate(sum=models.Sum('subtotal'))['sum'] or 0.00
        self.total_amount = total_amount
        if total_amount == 0.00:
            self.delete()
            return True
        else:
            self.save()
            return False

    def __str__(self):
        return f"Заказ #{self.id}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        permissions = [
            ("can_make_orders", "Can make orders"),
            ("can_view_orders", "Can view orders"),
            ("can_view_all_orders", "Can view all orders"),
        ]

admin.site.register(Order)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items", verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    subtotal = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Сумма")

    def save(self, *args, **kwargs):
        # Calculate the subtotal for the order item.
        self.subtotal = self.product.price * self.quantity
        super(OrderItem, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} ({self.quantity} шт.)"

    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказа"

admin.site.register(OrderItem)

# Create your models here.
