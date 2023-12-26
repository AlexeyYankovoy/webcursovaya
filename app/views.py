"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import PermissionDenied
from django.db import models
from .models import Blog
from .models import Comment
from .forms import CommentForm, BlogForm, ProductForm
from .models import Product
from .models import Category
from .models import Order, OrderStatus, OrderItem
from django.shortcuts import get_object_or_404

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

def catalog(request):
    assert isinstance(request, HttpRequest)
    categories = Category.objects.all()    
    return render(
        request, 
        'app/catalog.html',
        {
            'categories': categories,
            'title':'Каталог',
            'year':datetime.now().year,
        }
    )

def category(request, category_id):
    categories=Category.objects.all()
    category= get_object_or_404(Category, id=category_id)
    products=Product.objects.filter(category=category)
    return render(
        request,
        'app/category.html',
        {
            'categories': categories,
            'category':category,
            'products':products,
            'year':datetime.now().year,
        }
    )

def product(request, product_id):
    categories=Category.objects.all()
    assert isinstance(request, HttpRequest)
    product = Product.objects.get(id=product_id)
    return render(
        request, 
        'app/product.html', 
        {
            'categories': categories,
            'product': product,
            'title':'Информация о товаре',
            'year':datetime.now().year,
        }
    )

def cart(request):
    user = request.user
    try:
        active_order = Order.objects.get(user=user, is_sent=False)
    except Order.DoesNotExist:
        active_order = None
    if active_order:
        cart_items = active_order.order_items.all()
        total_price = sum(item.subtotal for item in cart_items)
    else:
        cart_items = []
        total_price = 0.00
    return render(
        request,
        'app/cart.html',
        {
            'cart_items': cart_items,
            'total_price': total_price,
            'year': datetime.now().year,
        }
    )

def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'error': 'Пользователь не аутентифицирован'}, status=401)  
        quantity = 1
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Продукт не найден'}, status=400)
        active_order, created = Order.objects.get_or_create(user=user, is_sent=False)
        order_item, created = OrderItem.objects.get_or_create(order=active_order, product=product)
        if not created:
            order_item.quantity += quantity
        order_item.save()
        return JsonResponse({'message': 'Продукт добавлен в корзину'})

def remove_from_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'error': 'Пользователь не аутентифицирован'}, status=401)
        try:
            item = OrderItem.objects.get(id=item_id)
        except OrderItem.DoesNotExist:
            return JsonResponse({'error': 'Продукт не найден'}, status=400)
        if not (user.has_perm('app.can_view_all_orders') or item.order.user == user):
            return JsonResponse({'error': 'Недостаточно прав'}, status=403)
        item.delete()
        order_deleted = item.order.update_total_amount()
        return JsonResponse({
            'message': 'Продукт удалён из корзины',
            'order_deleted': order_deleted
        })

def increase_quantity(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'error': 'Пользователь не аутентифицирован'}, status=401)
        try:
            item = OrderItem.objects.get(id=item_id)
            if not (user.has_perm('app.can_view_all_orders') or item.order.user == user):
                return JsonResponse({'error': 'Недостаточно прав'}, status=403)
            item.quantity += 1
            item.save()
            item.order.update_total_amount()
            return JsonResponse({'message': 'Количество увеличено успешно.'})
        except OrderItem.DoesNotExist:
            return JsonResponse({'message': 'Продукт не найден.'})

def decrease_quantity(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'error': 'Пользователь не аутентифицирован'}, status=401)
        try:
            item = OrderItem.objects.get(id=item_id)
            if not (user.has_perm('app.can_view_all_orders') or item.order.user == user):
                return JsonResponse({'error': 'Недостаточно прав'}, status=403)
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
                item.order.update_total_amount()
                return JsonResponse({'message': 'Количество уменьшено успешно.'})
            else:
                item.delete()
                order_deleted = item.order.update_total_amount()
                return JsonResponse({
                    'message': 'Продукт удален из корзины.',
                    'order_deleted': order_deleted
                })
        except OrderItem.DoesNotExist:
            return JsonResponse({'message': 'Продукт не найден.'})

def delete_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'error': 'Пользователь не аутентифицирован'}, status=401)
        if not user.has_perm('app.can_view_all_orders'):
            return JsonResponse({'error': 'Недостаточно прав'}, status=403)
        try:
            order = get_object_or_404(Order, id=order_id)
            order.delete()
            return JsonResponse({
                'message': 'Заказ успешно удален.',
                'order_deleted': True
            })
        except Order.DoesNotExist:
            return JsonResponse({'message': 'Заказ не найден.'})

def update_status(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        status_id = request.POST.get('status_id')
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'error': 'Пользователь не аутентифицирован'}, status=401)
        if not user.has_perm('app.can_view_all_orders'):
            return JsonResponse({'error': 'Недостаточно прав'}, status=403)
        try:
            order = get_object_or_404(Order, id=order_id)
            order.status = get_object_or_404(OrderStatus, id=status_id)
            order.save()
            return JsonResponse({
                'message': 'Статус обновлён.',
            })
        except Order.DoesNotExist:
            return JsonResponse({'message': 'Заказ/статус не найден.'})
        
def checkout(request):
    user = request.user
    try:
        active_order = Order.objects.get(user=user, is_sent=False)
        active_order.is_sent = True
        active_order.save()
        active_order.update_total_amount()
    except Order.DoesNotExist:
        pass
    return render(request, 'app/checkout.html')

def orders(request):
    if request.user.has_perm('app.can_view_all_orders'):
        orders = Order.objects.filter(is_sent=True)
        template_name = 'app/all_orders.html'
    elif request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user, is_sent=True)
        template_name = 'app/user_orders.html'
    else:
        orders = None
        template_name = 'app/index.html'
    return render(
        request,
        template_name,
        {
            'orders': orders, 
            'year': datetime.now().year,
        }
    )

def order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        template_name = 'app/order.html'
    except Order.DoesNotExist:
        pass
    user = request.user
    if not user.is_authenticated:
        raise PermissionDenied()
    statuses = OrderStatus.objects.all()
    return render(
        request,
        template_name,
        {
            'order': order,
            'year': datetime.now().year,
            'statuses': statuses,
        }
    )

def add_product(request):
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return redirect('catalog')
    else:
        product_form = ProductForm()
    return render(
        request,
        'app/add_product.html',
        {
            'product_form': product_form,
            'title': 'Добавить продукт',
            'year': datetime.now().year,
        }
    )

def error_403(request, exception):
    return render(
        request,
        'app/error.html',
        {
            'year': datetime.now().year,
            'info': 'Нет доступа',
        }
    )

def error_404(request, exception):
    return render(
        request,
        'app/error.html',
        {
            'year': datetime.now().year,
            'info': 'Страница не найдена',
        }
    )

def error_500(request):
    return render(
        request,
        'app/error.html',
        {
            'year': datetime.now().year,
            'info': 'Нет доступа',
        }
    )