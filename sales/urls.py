
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),


    path("products/", views.product_list, name="product_list"),
    path("product/add_product", views.add_product , name='add_product'),
    path("product/edit_prroduct/<str:sku>" , views.edit_product , name = 'edit_product' ),
    path("product/delete_product/<str:sku>" , views.delete_product , name = 'delete_product'),

    path("dealers/", views.dealer_list, name="dealer_list"),
    path("inventory/", views.inventory_list , name='inventory_list' ),
    path('order/', views.order_list , name='order_list')
]