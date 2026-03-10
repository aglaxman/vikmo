from django.shortcuts import render


def dashboard(req):
    return render(req,'dashboard.html')

def product_list(req):
    return render(req,'products/product_list.html')