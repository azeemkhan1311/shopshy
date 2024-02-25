from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
from . models import*
from django.contrib.auth.hashers import make_password, check_password


def index(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        # print(product_id)
        remove = request.POST.get('remove')

        cart_id = request.session.get('cart')
        if cart_id:
            quantity = cart_id.get(product_id)
            print(quantity)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart_id.pop(product_id)
                    else:
                        cart_id[product_id] = quantity - 1
                else:
                    print("i am here")
                    cart_id[product_id] = quantity + 1
            else:
                cart_id[product_id] = 1
        else:
            cart_id = {}
            cart_id[product_id] = 1
        request.session['cart'] = cart_id

    # print(request.session['cart'])
    category_obj = Category.objects.all()

    search_product = request.GET.get('search')
    search_product_by_category = request.GET.get('cat_id')
    if search_product:
        product_obj = Product.objects.filter(
            product_name__icontains=search_product)
    elif search_product_by_category:
        product_obj = Product.objects.filter(
            product_category=search_product_by_category)
    else:
        product_obj = Product.objects.all()

    global contents

    contents = {
        "category_obj": category_obj,
        "product_obj": product_obj,
    }
    return render(request, 'home.html', context=contents)


def validateCustomer(customer):
    error_message = None
    if (not customer.first_name):
        error_message = "Please Enter your First Name !!"
    elif len(customer.first_name) < 3:
        error_message = 'First Name must be 3 char long or more'
    elif not customer.last_name:
        error_message = 'Please Enter your Last Name'
    elif len(customer.last_name) < 3:
        error_message = 'Last Name must be 3 char long or more'
    elif not customer.mobile:
        error_message = 'Enter your Phone Number'
    elif len(customer.mobile) < 10:
        error_message = 'Phone Number must be 10 char Long'
    elif len(customer.password) < 5:
        error_message = 'Password must be 5 char long'
    elif len(customer.email) < 5:
        error_message = 'Email must be 5 char long'
    elif customer.isExists():
        error_message = 'Email Address Already Registered..'
    # saving

    return error_message


def signup(request):
    if request.method == 'POST':
        f_name = request.POST.get('fname')
        l_name = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('pwd')
        mobile = request.POST.get('mbl')
        gender = request.POST.get('gender')

        value = {
            'first_name': f_name,
            'last_name': l_name,
            'mobile': mobile,
            'email': email,
            'gender': gender
        }
        print(value)
        error_message = None

        customer = Signup(
            first_name=f_name,
            last_name=l_name,
            email=email,
            password=password,
            mobile=mobile,
            gender=gender)
        error_message = validateCustomer(customer)

        if not error_message:
            print(f_name, l_name, mobile, email, password, gender)
            customer.password = make_password(customer.password)
            customer.save()
            return redirect('home')
        else:

            data = {
                'error': error_message,
                'values': value,
                'category_obj': contents.get('category_obj'),
                'product_obj': contents.get('product_obj')
            }
            return render(request, 'home.html', data)

    #     sign_obj.save()

    # return render(request, 'signup.html')

#  login sysytem


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Signup.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['name'] = customer.first_name
                request.session['customer'] = customer.id

                return redirect('home')

            else:
                error_message = 'Wrong Passsword!!'
        else:
            error_message = 'please Enter valid Email !!'

        print(email, password)

        return render(request, 'home.html', {'error_message': error_message, 'category_obj': contents.get('category_obj'),
                                             'product_obj': contents.get('product_obj')})


def logout(request):
    request.session.clear()
    return redirect('home')


def cart_details(request):

    ids = request.session.get('cart').keys()

    cart_obj = Product.objects.filter(id__in=ids)

    context = {
        "cart_obj": cart_obj
    }
    return render(request, 'cart.html', context=context)


def checkout(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        customer_id = request.session.get('customer')
        print(customer_id)
        if not customer_id:
            return HttpResponse("please login")

        cart_obj = request.session.get('cart')

        product_obj = Product.objects.filter(id__in=list(cart_obj.keys()))

        for pro in product_obj:
            order_save = Order(
                address=address,
                mobile=mobile,
                customer=Signup(id=customer_id),
                product=pro,
                price=pro.product_price,
                quantity=cart_obj.get(str(pro.id))
            )
            order_save.save()

        return redirect('order')


def order(request):
    customer_id = request.session.get('customer')
    pro_obj = Order.objects.filter(customer=customer_id)
    tp = 0
    for i in pro_obj:
        tp = tp+(i.price*i.quantity)

    context = {
        'pro_obj': pro_obj,
        'tp': tp
    }
    request.session['cart'] = {}
    return render(request, 'order.html', context=context)
