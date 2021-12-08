from django.contrib import admin
from django.urls import path, include
from adminapp import views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.users, name='users'),
    path('users/create/', adminapp.user_create, name='user_create'),
    path('users/update/<int:pk>/', adminapp.user_update, name='user_update'),
    path('users/delete/<int:pk>/', adminapp.user_delete, name='user_delete'),

    path('categories/', adminapp.categories, name='categories'),
    path('categories/create/', adminapp.category_create, name='category_create'),
    path('categories/update/<int:pk>/', adminapp.category_update, name='category_update'),
    path('categories/delete/<int:pk>/', adminapp.category_delete, name='category_delete'),

    path('products/<int:pk>/', adminapp.products, name='products'),
    path('products/<int:pk>/create/', adminapp.product_create, name='product_create'),
    path('products/<int:category_pk>/update/<int:pk>/', adminapp.product_update, name='product_update'),
    path('products/<int:category_pk>/delete/<int:pk>/', adminapp.product_delete, name='product_delete'),
    path('products/<int:category_pk>/read/<int:pk>/', adminapp.product_read, name='product_read'),

]