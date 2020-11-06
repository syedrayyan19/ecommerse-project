from django.shortcuts import render, redirect

from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookieCart, guestOrder, cartData

# Create your views here.


def index(request):

    products = Products.objects.all()
    """data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']"""
    blogs = Blog.objects.all()
    feapd = products.filter(type='Featured Products')
    newpd = products.filter(type='New Products')
    inspd = products.filter(type='Inspired Products')

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookiedata=cookieCart(request)
        cartItems=cookiedata['cartItems']
    context = {'products': products,
               'blogs': blogs,
               'feapd': feapd,
               'newpd': newpd,
               'inspd': inspd,
               'cartItems': cartItems
               }
    return render(request, "index.html", context)


def category(request):
    product = Products.objects.all()
    cate = Products.objects.values('category').distinct()
    brand = request.POST.get('nike')
    color = request.POST.get('pink')
    if brand == 'on':
        product = product.filter(brand='nike')
    if color == 'on':
        product = product.filter(color='pink')

    return render(request, "category.html", {'product': product, 'cate': cate})


def cart(request):
    """data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items': items, 'order': order, 'cartItems': cartItems}"""
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except :
            cart={}
        print('CART:', cart)
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems=order['get_cart_items']
        for i in cart:
            #We use try block to prevent items in cart that may have been removed from causing error
            
            cartItems += cart[i]['quantity']
            product = Products.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']
            item={
                'product':{'id':product.id,'name':product.name,'price':product.price,'img':product.img},
                'quantity':cart[i]['quantity'],
                'get_total':total
            }
            items.append(item)


    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, "cart.html", context)


def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Products.objects.get(id=productId)
	order, created = Order.objects.get_or_create(
	    customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(
	    order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)


def blog(request):
    return render(request, "blog.html")


def tracking(request):
    return render(request, "tracking.html")


def contact(request):
    return render(request, "contact.html")


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        cookiedata = cookieCart(request)
        cartItems = cookiedata['cartItems']
        items = cookiedata['items']
        order = cookiedata['order']
    
    context = {'items': items, 'order': order,'cartItems':cartItems}
    return render(request, "checkout.html", context)


def productdetails(request, pk_test):
    prod = Products.objects.get(id=pk_test)
    pd = Products.objects.filter(type='New Products')
    return render(request, "single-product.html", {'prod': prod})

def processOrder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)
    var=data['shipping']
    print(var['number'])
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False,date_ordered=datetime.datetime.now())
    
    total=float(var['total'])
    order.transaction_id=transaction_id
    if total==order.get_cart_total:
        order.complete=True
    order.save()
    ShippingAddress.objects.create(customer=customer, order=order, number=var['number'], mail=var['mail'],add1=var['add1'],add2=var['add2'],city=var['city'],state=var['state'],pincode=var['zip'])
    return JsonResponse('payment subitted..',safe=False)
