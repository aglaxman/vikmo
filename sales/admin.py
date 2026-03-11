from django.contrib import admin

from .models import Product, Inventory,Order,OrderItem,Dealer


class InventoryAdmin(admin.ModelAdmin):
    list_display=('product','quantity')


class ProductAdmin(admin.ModelAdmin):
    list_display=('name','price')

class OrderItemAdmin(admin.ModelAdmin):
    readonly_fields = ('unit_price','line_total')  
    list_display = ('product','order_number','unit_price','quantity') 

    def order_number(self,obj):
        return obj.order.order_number

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('order_number','total_amount',)
    list_display = ('order_number','dealer','total_amount','status')

admin.site.register(Product,ProductAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Dealer)
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(Order,OrderAdmin)



