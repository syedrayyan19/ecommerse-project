from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth

# Create your views here.
def login(request):
    if request.method=='POST':
        email = request.POST['email']
        password = request.POST['pwd']
        user = auth.authenticate(request, username=email,password= password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'invalid details')
            return redirect('login')   
    else:
        return render(request,"login.html")

def register(request):
    if request.method=='POST':
        username = request.POST.get('username', False)
        email = request.POST['email']
        password1 = request.POST.get('pass')
        repassword = request.POST.get('repass')
        if password1== repassword:
            if User.objects.filter(email=email).exists():
                messages.info(request,'this email already registered')
                return redirect('register')
            else:
                
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                print('user created')
                return redirect('/')
        else:
            messages.info(request,'password not match')
            return redirect('register')
        return redirect('/')        
    else:
        
        return render(request, "registration.html")
def logout(request):
    auth.logout(request)
    return redirect('/')