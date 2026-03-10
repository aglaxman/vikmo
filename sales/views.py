from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse 
from django.db.models import Q

from .models import *

def dashboard(req):
    return render(req,'dashboard.html')

def product_list(req):

    query = req.GET.get('q')
    products = Product.objects.all()

    if query:
        products = Product.objects.filter(
            Q(name__icontains = query) |
            Q(sku__icontains = query)
        )
    context = {
        'products' : products,  
    }
    return render(req,'products/product_list.html' , context)

def add_product(req):

    if req.method == "POST":
        name = req.POST.get('name')
        sku = req.POST.get('sku')
        price = req.POST.get('price')
        description = req.POST.get('description')
        quantity = req.POST.get('stock')

        Product.objects.create(
            name = name,
            sku= sku,
            price = price,
            description = description
        )

        Inventory.objects.create(
            product = name,
            quantity = quantity
        )
        return redirect('product_list')
    return render(req, 'products/add_product.html')


def edit_product(req , sku):

    product = get_object_or_404(Product ,sku = sku)
    if req.method == "POST":
        product.name = req.POST.get('name')
        product.sku = req.POST.get('sku')
        product.price = req.POST.get('price')
        product.description = req.POST.get('description')

        product.save()
        return redirect(product_list)
    
    context = {
        'product' : product,
    }
    return render(req, 'products/edit_product.html', context)

def delete_product(req, sku):
    product = get_object_or_404(Product , sku=sku)
    product.delete()
    return redirect(product_list)


def dealer_list(req):
    dealers = Dealer.objects.all()
    context = {
        'dealers' : dealers,  
    }
    return render(req,'dealers/dealer_list.html', context)


def inventory_list(req):
    inventories = Inventory.objects.all()
    context = {
        'inventories' : inventories,  
    }
    return render(req,'inventory/inventory_list.html', context)


def order_list(req):
    orders = Order.objects.all()
    context = {
        'orders' : orders,  
    }
    return render(req, 'order/order_list.html', context)
