"""
Definition of urls for Mechboards.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin, staticfiles
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings


urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Войти',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('registration/', views.registration, name='registration'),
    path('news/', views.news, name='news'),
    path('newspost/<int:parametr>/', views.newspost, name='newspost'),
    path('newpost/', views.newpost, name='newpost'),
    path('catalog/', views.catalog, name='catalog'),    
    path('category/<int:category_id>/', views.category, name='category'),
    path('product/<int:product_id>/', views.product, name='product'),    
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    path('increase_quantity/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/', views.decrease_quantity, name='decrease_quantity'),
    path('delete_order/', views.delete_order, name='delete_order'),
    path('update_status/', views.update_status, name='update_status'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.orders, name='orders'),
    path('order/<int:order_id>', views.order, name='order'),
    path('add_product/', views.add_product, name='add_product'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

handler403 = views.error_403
handler404 = views.error_404
handler500 = views.error_500
