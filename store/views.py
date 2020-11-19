from django.shortcuts import render, redirect, get_object_or_404
from .models import Product ,Category,Cart,CartItem
from django.contrib.auth.models import Group,User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate,logout
from .forms import SignUpForm


# Create your views here.
def home(request ,category_slug=None):
    category_page =None
    if category_slug:
        products = Product.objects.filter(category__slug=category_slug, available=True) # same as blow lines
        # category_page= Category.objects.filter(slug=category_slug)
        # products = Product.objects.filter(slug=category_slug, available=True)
    else:
        products =Product.objects.filter(available=True).order_by('price')
    # links=Category.objects.all()

    context = { category_page:'category','products' : products} #'links':links}
    return render(request , 'index.html', context)

def productDetail(request ,category_slug,product_slug):
    # try:
    product =Product.objects.get(category__slug=category_slug, slug=product_slug)
    context = {'product' : product}
    return render(request , 'product.html' , context)

def category(request):
    category=Category.objects.all()
    return render(request,'navbar.html',{'category':category})


def about(request):
    return render(request , 'about.html' )

def cart(request):
    return render(request , 'cart.html',{} )

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart= request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    cart ,created = Cart.objects.get_or_create(cart_id=_cart_id(request))
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity< cart_item.product.stock:
            cart_item.quantity += 1
            cart_item.save()

    except CartItem.DoesNotExist:
        cart_item= CartItem.objects.create(product=product,cart=cart ,quantity=1)
        cart_item.save()
    return redirect('cart_detail')


def cart_detail(request ,total=0 ,counter=0,cart_items=None):
    try:
        cart= Cart.objects.get(cart_id=_cart_id(request))
        cart_items =CartItem.objects.filter(cart=cart , active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter= cart_item.quantity
    except CartItem.DoesNotExist:
        pass
    return render(request, 'cart.html' ,dict(cart_items=cart_items,total=total,counter=counter))


def cart_remove(request ,product_id):
    cart= Cart.objects.get(cart_id=_cart_id(request))
    product= get_object_or_404(Product,id=product_id)
    cart_item =CartItem.objects.get(product=product,cart=cart)
    if cart_item.quantity> 1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_detail')



def cart_remove_product(request,product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart_detail')

def thank_page(request):
    return render(request ,'thanks.html',{})
def search(request):
    return render(request ,'home.html',{})


def signUpView(request):
    if request.method =='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username =form.cleaned_data.get('username')
            signup_user = User.objects.get(username=username)
            customer_group =Group.objects.get(name="Customer")
            customer_group.user_set.add(signup_user)
            #login(request,signup_user)
    else:
        form =SignUpForm()
    return render(request,'signup.html',{'form':form})


def signInView(request):
    #from .forms import SignUpForm
    if request.method =='POST':
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            username=request.POST['username']
            password=request.POST['password']
            user= authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('index')

            else:
                return redirect('signup')

    else:
        form =AuthenticationForm()

    return render(request,'signin.html',{'form':form})



def signoutView(request):
    logout(request)
    return redirect('signin')


def search(request):
    products= Product.objects.filter(name__contains=request.GET['title'])
    return render(request,'index.html',{'products': products})