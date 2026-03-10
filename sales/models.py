from django.db import models
from django.utils import timezone
# Create your models here.

class Product(models.Model):

    
    name = models.CharField(max_length=250,null=False)
    sku = models.CharField(max_length=100,unique=True)
    price = models.DecimalField(max_digits=10 , decimal_places=2, null=False)
    description  = models.TextField(max_length=400 , null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    
class Inventory(models.Model):

    
    product = models.OneToOneField(Product , on_delete=models.CASCADE,related_name="inventory")
    quantity = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name}"
    
    class Meta:
        verbose_name_plural = "Inventory"
    

class Dealer(models.Model):
    
    
    name = models.CharField(max_length=150, null=False)
    email = models.EmailField()
    phone = models.CharField(max_length=15, null = False)
    address = models.TextField(max_length=500, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Order(models.Model):

    order_number = models.CharField(max_length=30, unique=True, blank=True)
    status_choices = [
            ('draft','Draft'),
            ('confirmed','Confirmed'),
            ('delivered','Delivered')
        ]
  
    dealer = models.ForeignKey(Dealer , on_delete=models.CASCADE)
    status = models.CharField(max_length=20,choices= status_choices, default='draft')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Order {self.order_number}"


    def save(self, *args, **kwargs):

        if not self.order_number:

            today = timezone.now().strftime("%Y%m%d")

            last_order = Order.objects.filter(
                order_number__startswith=f"ORD-{today}"
            ).order_by("order_number").last()

            if last_order:
                last_number = int(last_order.order_number.split("-")[-1])
                new_number = last_number + 1
            else:
                new_number = 1

            self.order_number = f"ORD-{today}-{new_number:04d}"

        super().save(*args, **kwargs)


class OrderItem(models.Model):

    
    order = models.ForeignKey(Order, on_delete=models.CASCADE , related_name='items' )
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    line_total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    def save(self, *args, **kwargs):

        # take price from product automatically
        if not self.unit_price:
            self.unit_price = self.product.price

        # calculate line total
        self.line_total = self.quantity * self.unit_price

        super().save(*args, **kwargs)

        # recalculate order total
        order_total = sum(
            item.line_total for item in self.order.items.all()
        )

        self.order.total_amount = order_total
        self.order.save(update_fields=["total_amount"])


    
