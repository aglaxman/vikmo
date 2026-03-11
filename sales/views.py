from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse 
from django.db.models import Q

from .models import *

def dashboard(req):
    return render(req,'dashboard.html')




# -------------------------------------------------------------------------------


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

        if Product.objects.filter(sku = sku).exists():

            return render(req , 'products/add_product.html',{
                'error':'SKU already exists. Please try to use other SKU'
            })
        
        product=Product.objects.create(
            name = name,
            sku= sku,
            price = price,
            description = description
        )

        Inventory.objects.create(
            product = product,
            quantity = quantity
        )
        return redirect('product_list')
    return render(req, 'products/add_product.html')


def edit_product(req , sku):

    product = get_object_or_404(Product ,sku = sku)

    if req.method == "POST":
        name = req.POST.get('name')
        new_sku = req.POST.get('sku')
        price = req.POST.get('price')
        description = req.POST.get('description')

        if Product.objects.filter(sku = new_sku).exclude(pk=product.pk).exists():
            return render(req , 'products/edit_product.html',{
                'product' : product,
                'error':'SKU already exists. Please try to use other SKU'
            })

        product.name = name
        product.sku = new_sku
        product.price = price
        product.description = description

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


# -------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------

def dealer_list(req):

    query = req.GET.get('q')
    dealers = Dealer.objects.all()

    if query:
        dealers = Dealer.objects.filter(
            Q(email__icontains = query) |
            Q(name__icontains = query) |
            Q(phone__icontains = query)
        )

    context = {
        'dealers' : dealers,  
    }
    return render(req,'dealers/dealer_list.html', context)

def add_dealer(req):

    if req.method == 'POST':
        name = req.POST.get('name')
        email = req.POST.get('email')
        phone = req.POST.get('phone')
        address  = req.POST.get('address')

        if Dealer.objects.filter(Q(email = email) | Q(phone = phone) ).exists():
            return render(req, 'dealers/add_dealer.html',{
                'error' : 'Email or Phone number already  Exists..'
            })

        Dealer.objects.create(
            name = name,
            email = email,
            phone = phone,
            address = address
        )

        return redirect(dealer_list)
    return render(req, 'dealers/add_dealer.html')


def edit_dealer(req , pk ):
    dealer = get_object_or_404(Dealer , pk = pk)

    if req.method == 'POST':
        name = req.POST.get('name')
        new_email = req.POST.get('email')
        new_phone = req.POST.get('phone')
        address = req.POST.get('address')

        if Dealer.objects.filter(Q(email = new_email) | Q(phone = new_phone)).exclude(pk=dealer.pk).exists():
            return render(req, 'dealers/edit_dealer.html',{
                'dealer':dealer,
                'error':'Email or Phone numbe already exists.'
            })
        
        dealer.name = name
        dealer.email = new_email
        dealer.phone = new_phone
        dealer.address = address

        dealer.save()

        return redirect('dealer_list')
    
    context = {
        'dealer' : dealer,
    }

    return render(req, 'dealers/edit_dealer.html', context)


def delete_dealer(req, pk):
    dealer = get_object_or_404(Dealer , pk = pk)
    dealer.delete()
    return redirect(dealer_list)
    

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
