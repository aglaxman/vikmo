from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse 
from django.db.models import Q
from django.contrib import messages

from .models import *




def confirm_order(order):

    # 1️⃣ Validate stock first
    for item in order.items.all():

        inventory = item.product.inventory

        if item.quantity > inventory.quantity:
            raise ValueError(
                f"Not enough stock for {item.product.name}. Available: {inventory.quantity}"
            )

    # 2️⃣ Reduce stock only after validation passes
    for item in order.items.all():

        inventory = item.product.inventory
        inventory.quantity -= item.quantity
        inventory.save()

    # 3️⃣ Update order status
    order.status = "confirmed"
    order.save()

def validate_stock(product_ids, quantities):

    errors = []

    for i in range(len(product_ids)):

        product = Product.objects.get(id=product_ids[i])
        inventory = product.inventory
        qty = int(quantities[i])

        if qty > inventory.quantity:

            errors.append(
                f"{product.name} → Available stock: {inventory.quantity}, Requested: {qty}"
            )
    if errors:
        raise ValueError(errors)
        



def dashboard(req):
    return render(req,'dashboard.html')



# Product CRUD Operations
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

        return redirect('product_list')
    context = {
        'product' : product,
    }
    return render(req, 'products/edit_product.html', context)


def delete_product(req, sku):
    product = get_object_or_404(Product , sku=sku)
    product.delete()
    return redirect('product_list')


# ---------------------------------xxxxxxxxxxxxxxxxxxxxx--------------------------------------------


# Dealer CRUD Operations
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
    return redirect('dealer_list')


#-----------------------------------xxxxxxxxxxxxxxxxxxxx--------------------------
    

def inventory_list(req):

    query  = req.GET.get('q')
    inventories = Inventory.objects.all()

    if query:
        inventories = Inventory.objects.filter(
           Q(product__name__icontains = query) |
           Q(product__sku__icontains = query)
        )
    context = {
        'inventories' : inventories,  
    }
    return render(req,'inventory/inventory_list.html', context)



#----------------------xxxxxxxxxxxxxxxxxxxxxx------------------------------


def order_list(req):

    query = req.GET.get('q')
    orders = Order.objects.all()

    if query:

        orders = Order.objects.filter(
            Q(order_number__icontains = query) |
            Q(dealer__name__icontains = query)
        )
    context = {
        'orders' : orders,  
    }
    return render(req, 'order/order_list.html', context)




def create_order(req):

    order_number = Order.generate_order_number()
    dealers = Dealer.objects.all()
    products = Product.objects.all()

    if req.method == "POST":

        dealer_id = req.POST.get("dealer")

        product_ids = req.POST.getlist("product_id[]")
        quantities = req.POST.getlist("quantity[]")
        prices = req.POST.getlist("price[]")

        # call validation
        if "place_order" in req.POST:
            try:
                validate_stock(product_ids, quantities)
            except ValueError as e:

                for error in e.args[0]:
                    messages.error(req, error)

                return redirect("create_order")

        order = Order.objects.create(
            order_number=order_number,
            dealer_id=dealer_id,
            status="draft"
        )

        for i in range(len(product_ids)):
            OrderItem.objects.create(
                order=order,
                product_id=int(product_ids[i]),
                quantity=int(quantities[i]),
                unit_price=float(prices[i]),
            )

        if "place_order" in req.POST:
            confirm_order(order)

        return redirect("order_list")

    context = {
        "order_number": order_number,
        "dealers": dealers,
        "products": products,
    }

    return render(req, "order/create_order.html", context)



def edit_order(req, pk):

    order = get_object_or_404(Order, pk=pk)
    orderitems = order.items.all()
    products = Product.objects.all()

    if req.method == "POST":

        product_ids = req.POST.getlist("product_id[]")
        quantities = req.POST.getlist("quantity[]")
        prices = req.POST.getlist("price[]")

        # validate stock if placing order
        if "place_order" in req.POST:
            try:
                validate_stock(product_ids, quantities)
            except ValueError as e:

                for error in e.args[0]:
                    messages.error(req, error)

                return redirect("edit_order", pk=order.pk)

        # delete old items
        order.items.all().delete()

        # create updated items
        for i in range(len(product_ids)):
            OrderItem.objects.create(
                order=order,
                product_id=int(product_ids[i]),
                quantity=int(quantities[i]),
                unit_price=float(prices[i]),
            )

        # confirm order if requested
        if "place_order" in req.POST:
            confirm_order(order)

        return redirect("order_list")

    context = {
        "order": order,
        "orderitems": orderitems,
        "products": products,
    }

    return render(req, "order/edit_order.html", context)





def view_order(req, pk):
    order = get_object_or_404(Order , pk = pk)
    orderitems = OrderItem.objects.filter(order = order)
    products = Product.objects.all()


    if req.method == "POST":
        product_ids = req.POST.getlist("product_id[]")
        quantities = req.POST.getlist("quantity[]")
        prices = req.POST.getlist("price[]")

        # delete old items
        order.items.all().delete()

        for i in range(len(product_ids)):
            OrderItem.objects.create(
                order=order,
                product_id=int(product_ids[i]),
                quantity=int(quantities[i]),
                unit_price=float(prices[i]),
            )

        if "place_order" in req.POST:
            try:
                confirm_order(order)
            except ValueError as e:
                messages.error(req, str(e))
                return redirect("create_order")
              
        return redirect("order_list")


    context = {

        'order' : order,
        'orderitems' : orderitems,
        'products' : products,

    }
    return render(req , 'order/view_order.html' , context)

def delete_order(req, pk):
    order = get_object_or_404(Order , pk = pk)
    order.delete()
    return redirect('order_list')