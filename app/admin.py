from django.contrib import admin

# Register your models here.
from .models import *



from .models import Cart, Customer, OrderPlaced, Product, BuyOrder, Order 




@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','locality','city','zipcode','state']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display= ['id','title','selling_price','discounted_price','description','brand','category','product_image']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']
    
@admin.register(BuyOrder)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer','product','quantity','order_date','status']



@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered','created', 'paymentId','orderId']
    
    

admin.site.register(Transaction)
admin.site.register(PaymentGatewaySettings)

