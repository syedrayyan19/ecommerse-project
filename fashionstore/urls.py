from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index, name="index"),
    path('category', views.category, name="category"),
    path('cart/', views.cart, name="cart"),
    path('blog', views.blog, name="blog"),
    path('tracking', views.tracking, name="tracking"),
    path('update_item/', views.updateItem, name="update_item"),
    path('contact', views.contact, name="contact"),
    path('checkout/', views.checkout, name="checkout"),

    path('process_order/', views.processOrder, name="process_Order"),

    path('product-details/<str:pk_test>/', views.productdetails, name="product-details"),
   
]
