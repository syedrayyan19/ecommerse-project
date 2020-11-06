from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Products(models.Model):
    TY=(
        ('Featured Products','Featured Products'),
        ('New Products','New Products'),
        ('Inspired Products','Inspired Products'),
        )
    
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='img')
    price = models.FloatField()
    delprice= models.FloatField()
    type=models.CharField(max_length=200, choices=TY)
    category=models.CharField(max_length=100,null=True)
    brand=models.CharField(max_length=100,null=True)
    color=models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.name
    
class Blog(models.Model):
    
    title = models.TextField(max_length=100)
    desc = models.TextField(max_length=500)
    date=models.DateTimeField(auto_now=False)
    blogimage= models.ImageField(upload_to='img')


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now=False, null=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
	product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True, blank=True)
    number=models.CharField(max_length=100, null=True)
    mail = models.CharField(max_length=200, null=True)
    add1 = models.CharField(max_length=200, null=True)
    add2 = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    pincode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(max_length=200, null=True)

    def __str__(self):
        return self.number
class Cart(models.Model):
    cart_name = models.CharField(max_length=100, null=True)
    cart_img = models.ImageField(upload_to='img', null=True)
    cart_price = models.FloatField(null=True)
