
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),

# ------------------------------------------------------------------------------------------------

    path("products/", views.product_list, name="product_list"),
    path("product/add_product", views.add_product , name='add_product'),
    path("product/edit_product/<str:sku>" , views.edit_product , name = 'edit_product' ),
    path("product/delete_product/<str:sku>" , views.delete_product , name = 'delete_product'),

# --------------------------------------------------------------------------------------------------


    path("dealers/", views.dealer_list, name="dealer_list"),
    path('dealer/add_dealer', views.add_dealer, name = 'add_dealer'),
    path('dealer/edit_dealer/<int:pk>' , views.edit_dealer , name= 'edit_dealer'),
    path('dealer/delete_dealer/<int:pk>' , views.delete_dealer , name = 'delete_dealer'),



    path("inventory/", views.inventory_list , name='inventory_list' ),




    path('order/', views.order_list , name='order_list'),
    path('order/genrate_order_number/', views.genreate_order_number , name='genreate_order_number'),
    path('order/create_order/<int:pk>' , views.create_order ,name= 'create_order'),
]