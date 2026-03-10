from django.db import models

# Create your models here.

class Product(models.Model):

    id = models.IntegerField(max_length=100,unique=True)
    name = models.CharField(max_length=250,null=False)
    sku = models.IntegerField(unique=True)
    price = models.DecimalField(max_length=100 , null=False)
    description  = models.TextField(max_length=400 , null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.product_name
    
class Inventry(models.Model):

    id = models.IntegerField(max_length=100, unique=True)
    product = models.OneToOneField(Product)
    quantity = models.IntegerField(max_length=5, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.inventry_id

class Dealer(models.Model):
    
    id = models.IntegerField(max_length=100,unique=True)
    name = models.CharField(max_length=150, null=False)
    email = models.CharField(max_length=150 , null=False)
    phone = models.IntegerField(max_length=10, null = False)
    address = models.TextField(max_length=500, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Order(models.Model):

    id = models.IntegerField(max_length=100 ,unique=True)
    dealer = models.ForeignKey(Dealer)
    status = models.CharField(
        choices=[
            ('draft','Draft'),
            ('confirmed','Confirmed'),
            ('delivered','Delivered')
        ]
    )

    total_amount = 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id
    

class OrderItem(models.Model):

    id = models.IntegerField(max_length=100 , unique=True)
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(max_length=100, null=False)
    unit_price = models.ForeignKey(Product.price)
    line_total = 


    def __str__(self):
        return self.id
