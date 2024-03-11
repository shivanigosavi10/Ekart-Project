from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Product,Cart,Order, MyOrder
from django.db.models import Q
import random
import razorpay
from django.core.mail import send_mail

# Create your views here.
def hello(request):
     return render(request,"base.html")

def register(request):
 context={}
 if request.method == "POST":
          name=request.POST["uname"]
          upass1=request.POST["upass"]
          upass2=request.POST["ucom"]
          if name==' ' or upass1=='' or upass2=='':
            context['errmsg']="Feild cannot be empty!!!"
            return render(request,'register.html',context)
          elif upass1!= upass2:
            context['errmsg']="Password and Confirm password not matched!!!"
            return render (request,'register.html',context)
          else:
            try:     
               u=User.objects.create(username=name,email=name,password=upass1)
               u.set_password(upass1)
               u.save()
               context['success']="register succesfully!!!"
               return render (request,'register.html',context)
            except Exception:
                 context['errmsg']="Username alredy Exist"
                 return render(request, "register.html",context)
 else:
    return render(request, "register.html")
    



def user_login(request):
     context={}
     if request.method=="POST":
            user_name=request.POST['uname']
            pwd=request.POST['pass']
            if user_name=='' or pwd=='':
                context['errmsg']="field can not be empty"
                return render(request,"login.html",context)
            else:
                u=authenticate(username=user_name,password=pwd)
                if u is not None:
                    login(request,u)
                    print(request.user.is_authenticated)
                    return redirect('/home')
                else:
                    context['errmsg']="Invalid username and password!!"
                    return render(request,"login.html",context)
                
     else:
         return render(request,"login.html")
                

def home(request):
     return render(request,"index.html")

def about(request):
     return render(request,"about.html")

def contact(request):
     return render(request,"contact.html")


def product(request):
    context={}
    uid=request.user.id
    products=Product.objects.filter(is_active=True)
#   context['prod']=p
    context['product']=products
    return render(request,'index.html',context)

def catfilter(request,cv):
    q1=Q(cat=cv)
    q2=Q(is_active=True)

    context={}
    print(cv)
    products=Product.objects.filter(q1&q2)
    context['product']=products
#     print(prod)
    
    return render(request,'index.html',context)
#     return HttpResponse(cv)
    
def sortprice(request,sv):
     if sv == '1':
        products=Product.objects.order_by("-price").filter(is_active=True)
     else:
         products=Product.objects.order_by("price").filter(is_active=True)
    
     context={}
     context['product']=products
     return render(request,"index.html",context)

def filterbyprice(request):
    min=request.GET["min"]
    max=request.GET["max"]
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    products=Product.objects.filter(q1&q2&q3)
    context={}
    context["product"]=products
#     print(min,max)
    return render(request, "index.html",context)

def pdetails(request,pid):
    p = Product.objects.filter(id = pid)
    context = {}
    context['data'] = p
    return render(request,"products_details.html",context)



def placeorder(request):
     return render(request,"placeorder.html")

def user_logout(request):
     logout(request)
     return redirect("/login")

# def viewcart(request):
#      return render(request,"cart.html")

def cart(request,pid):
    if request.user.is_authenticated:
        u = User.objects.filter(id = request.user.id)
        # print(u[0])
        # return HttpResponse("User Fetched !!")
        p = Product.objects.filter(id = pid)
        q1 = Q(user_id = u[0])
        q2 = Q(pid = p[0])
        c = Cart.objects.filter(q1 & q2)
        n = len(c)
        context = {}
        context['data'] = p
        if n > 1:
            context['msg'] = 'Product already exist in the cart'
            return render(request, "products_details.html", context)
        else:
            c = Cart.objects.create(user_id = u[0],pid= p[0])
            c.save()
            context['msg_success'] = "Product sucessfully added to the alert"
            return render (request, "products_details.html",context)
            
    else:
        return redirect("/login")
    

def viewcart(request):
    c = Cart.objects.filter(user_id = request.user.id)
    tot = 0
    for x in c:
        tot = tot + x.pid.price * x.qty
    context = {}
    context['data'] = c
    context['tot'] = tot
    context['n'] = len(c)
    return render(request,"cart.html", context)

def remove(request,cid):
    c = Cart.objects.filter(id = cid)
    c.delete()
    return redirect("/view_cart")

def updateqty(request, x, cid):
    c = Cart.objects.filter(id = cid)
    q = c[0].qty
    if x == '1':
        q = q+1
    elif q>1:
        q = q-1
    c.update(qty = q)
    return redirect("/view_cart")

def placeorder(request):
    c = Cart.objects.filter(user_id = request.user.id)
    oid = random.randrange(1000, 9999)
    for x in c:
        amount = x.pid.price * x.qty
        o = Order.objects.create(order_id = oid, user_id = x.user_id, pid = x.pid, qty= x.qty, amt=amount)
        o.save()
        x.delete()
    return redirect("/fetchorder")

def fetchorder(request):
    o = Order.objects.filter(user_id = request.user.id)
    tot=0
    for x in o:
        tot=tot+x.amt
    context={}
    context['data']=o
    context['tot']=tot
    context['n']=len(o)
    return render(request,'placeorder.html',context)

def makepayment(request):
    client = razorpay.Client(auth=("rzp_test_R7kWkFU6ZllnWF", "W0gE85soRmV6WanAQr1nW69n"))
    ord = Order.objects.filter(user_id = request.user.id)
    tot = 0
    print(ord)
    for x in ord:
        tot = tot + x.amt
        oid = x.order_id
    data = {"amount":tot*100, "currency":"INR", "receipt": oid}
    payment = client.order.create(data = data)
    print(payment)
    context = {}
    context['payment'] = payment
    return render(request, "pay.html",context)

def paymentsuccess(request):
    sub = "Ekart Order Status"
    msg = "Thank for Shopping"
    u = User.objects.filter(id = request.user.id)
    to = u[0]  # to fetch the email id
    print(to)
    frm = "shivanigosavi943@gmail.com"

    send_mail(
    sub,
    msg,
    frm,
    [to],
    fail_silently=False,
)    
    ord = Order.objects.filter(user_id = u[0])
    for x in ord:
        mo = MyOrder.objects.create(order_id = x.order_id, user_id = x.user_id, pid = x.pid, amt = x.amt, qty = x.qty)
        mo.save()
    x.delete()
    return HttpResponse('payment success !!')