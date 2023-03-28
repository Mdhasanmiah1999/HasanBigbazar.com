from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

STATE_CHOICES = (
    ('Cumilla', 'Cumilla'),
    ('Dhaka','Dhaka')
)

class Customer(models.Model):
 user = models.ForeignKey(User, on_delete=models.CASCADE)
 name = models.CharField(max_length=200)
 locality = models.CharField(max_length=200)
 city = models.CharField(max_length=50)
 zipcode = models.IntegerField()
 state = models.CharField(choices=STATE_CHOICES, max_length=50)
 def __str__(self):
  return str(self.id)


CATEGORY_CHOICES = (
    ('M', 'Mobile'),
    ('L', 'Laptop'),
    ('TW', 'Top Wear'),
    ('BW', 'Bottom Wear'),
)
class Product(models.Model):
 #name = models.CharField(max_length=255)
 #name=models.CharField(max_length=225)
 title = models.CharField(max_length=100)
 selling_price = models.FloatField()
 discounted_price =  models.FloatField()
 description = models.TextField()
 brand = models.CharField(max_length=100)
 category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
 product_image = models.ImageField(upload_to = 'productimg')

 def __str__(self):
  return str(self.id) 

@property
def total_cost(self):
 return self.quantity * self.product.discounted_price

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

class BuyOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way',),
    ('delivered','delivered'),
    ('cancel','cancel')
    
)



    



class OrderPlaced(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices = STATUS_CHOICES,default='Pending')
    




    
class Order(models.Model):
    PAYMENT_METHOD = (
        ('Cash on Delevery', 'Cash on Delivery'),
        ('paypal','Paypal'),
        ('SSLcommerz', 'SSLcommerz'))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #orderitems = models.ManyToManyField(Cart)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    paymentId = models.CharField(max_length=255, blank=True, null=True)
    orderId = models.CharField(max_length=255, blank=True, null=True)
    payment_method = models.CharField(max_length=30, choices = PAYMENT_METHOD, default= 'Cash on Delevery')
    
    def get_totals(self):
        total = 0
        for order_item in self.orderitems.all():
            if order_item.variation_total():
                total+= float(order_item.variation_total())
            elif order_item.variation_single_price():
                total+= float(order_item.variation_single_price())
            else:
                total+= float(order_item.get_total())
        return total
        



class Profile(models.Model):
    user = models.OneToOneField(User ,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20)
    otp = models.CharField(max_length=6)



@property
def total_cost(self):
 return  self.product.discounted_price


class Transaction(models.Model):

    # user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # biling_profile = models.ForeignKey(Billing, on_delete=models.DO_NOTHING)
    # products    = models.ManyToManyField(Course, blank=True)
    name = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tran_id = models.CharField(max_length=15)
    val_id = models.CharField(max_length=75)
    card_type = models.CharField(max_length=150)
    store_amount = models.DecimalField(max_digits=10, decimal_places=2)
    card_no = models.CharField(max_length=55, null=True)
    bank_tran_id = models.CharField(max_length=155, null=True)
    status = models.CharField(max_length=55)
    tran_date = models.DateTimeField()
    currency = models.CharField(max_length=10)
    card_issuer = models.CharField(max_length=255)
    card_brand = models.CharField(max_length=15)
    card_issuer_country = models.CharField(max_length=55)
    card_issuer_country_code = models.CharField(max_length=55)
    currency_rate = models.DecimalField(max_digits=10, decimal_places=2)
    verify_sign = models.CharField(max_length=155)
    verify_sign_sha2 = models.CharField(max_length=255)
    risk_level = models.CharField(max_length=15)
    risk_title = models.CharField(max_length=25)
   


    # def __str__(self):
    #     return self.user.username

        
class PaymentGatewaySettings(models.Model):

    store_id = models.CharField(max_length=500, blank=True, null=True)
    store_pass = models.CharField(max_length=500, blank=True, null=True)
    
    class Meta:
        verbose_name = "PaymentGatewaySetting"
        verbose_name_plural = "PaymentGatewaySettings"
        db_table = "paymentgatewaysettings"
