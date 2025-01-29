import re
import hashlib
import razorpay 
from urllib import request
from django.conf import settings
from django.http import Http404, HttpResponse, JsonResponse
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from core.forms import *
from core.models import *
from .models import Product, Category
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.contrib.postgres.search import SearchVector


# Create your views here.

razorpay_client =razorpay.Client(auth=(settings.RAZORPAY_ID,settings.RAZORPAY_SECRET))



def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request,'core/index.html',{'products':products,'categories':categories,'title':'Accu-Mart | Hospital Equipment Manufacturer'})

def about(request):
    categories = Category.objects.all()
    return render(request,'core/about.html',{'categories':categories,'title':'Accu-Mart | About'})

def certification(request):
    categories = Category.objects.all()
    return render(request,'core/certifications.html',{'categories':categories,'title':'Accu-Mart | Certification'})

def refund_policy(request):
    categories = Category.objects.all()
    return render(request,'core/refund_policy.html',{'categories':categories,'title':'Accu-Mart | Cancellation, Return & Refund Policy'})

    # return render(request,'core/refund_policy.html')

def terms_and_conditions(request):
    categories = Category.objects.all()
    return render(request,'core/terms_and_condition.html',{'categories':categories,'title':'Accu-Mart | Terms & Conditions'})

    # return render(request,'core/terms_and_condition.html')

def shipping_policy(request):
    categories = Category.objects.all()
    return render(request,'core/shipping_policy.html',{'categories':categories,'title':'Accu-Mart | Shipping Policy'})


def disclaimer(request):
    categories = Category.objects.all()
    return render(request,'core/disclaimer.html',{'categories':categories,'title':'Accu-Mart | Disclaimer'})

# view cart start
def view_cart(request):
    categories = Category.objects.all()

    if Order.objects.filter(user=request.user, ordered=False).exists():
        order = Order.objects.get(user=request.user, ordered=False)
        
        order.subtotal_price = order.get_subtotal_price()
        order.total_price = order.get_total_price()
        order.total_gst = order.get_total_gst()
        
        order.save()

        return render(request, 'core/checkout/view_cart.html', {
            'order': order,
            'categories': categories
        })

    return render(request, 'core/checkout/view_cart.html', {'message': 'Your Cart is Empty!','categories':categories,'title':'Accu-Mart | Cart'})
# view cart end

# update_cart start
def update_cart(request):
    if request.method == 'POST':
        order_item_id = request.POST.get('order_item_id')
        quantity = int(request.POST.get('quantity'))

        order_item = get_object_or_404(OrderItem, id=order_item_id)

        order_item.quantity = quantity
        order_item.save()

        order = order_item.user.order_set.filter(ordered=False).first()  # Get the active order
        if order:
            order.subtotal_price = order.get_subtotal_price()
            order.total_price = order.get_total_price()
            order.total_gst = order.get_total_gst()
            order.save()

        # Return updated cart data as JSON
        return JsonResponse({
            'subtotal_price': round(order.subtotal_price, 2),
            'total_price': round(order.total_price, 2),
            'total_gst': round(order.total_gst, 2),
            'item_count': order.items.count(),
        })
# update cart end
    
# add product start
def add_product(request):
    categories = Category.objects.all()
    if request.method == 'POST':
       form = ProductForm(request.POST, request.FILES) 
       if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('/')
       else:
           messages.error(request, 'PLEASE CHECK THE DETAILS.')
           messages.info(request,'PRODUCT IS NOT  ADDED...........')
    #    return redirect('/')
    else:
        form = ProductForm()
    return render(request,'core/products/add_product.html',{'form':form,'categories':categories,'title':'Accu-Mart | Add Product'})
# add product end
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    categories=Category.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_desc', product.id)
    else:
        form = ProductForm(instance=product)

    return render(request, 'core/products/edit_product.html', {'form': form, 'product': product,'categories':categories,'titile':'Accu-Mart | Edit Product'})

def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    categories = Category.objects.all()
    if request.method == 'POST':
        # print("product deleted")
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('all_products')  # Redirect to product list after deletion

    return render(request, 'core/products/product_detail.html', {'product': product,'categories':categories})

# product description start
def product_desc(request, pk):
    product = Product.objects.get(pk=pk)
    categories = Category.objects.all()
    category = product.category
    
    # Split the specifications into key-value pairs
    specifications = []
    box_contain =[]
    if product.specifications:
        for spec in product.specifications.splitlines():
            # Check if each line contains a colon (to split into key-value pair)
            if ":" in spec:
                key, value = spec.split(":", 1)  # Split only on the first colon
                specifications.append((key.strip(), value.strip()))  # Strip extra spaces
            else:
                specifications.append((spec.strip(),))  
    if product.box_contain:
        for spec in product.box_contain.splitlines():
            
            if ":" in spec:
                key, value = spec.split(":", 1)  
                box_contain.append((key.strip(), value.strip()))  
            else:
                box_contain.append((spec.strip(),))  
    

    return render(request, 'core/products/product_detail.html', {
        'product': product,
        'category': category,
        'specifications': specifications,  # Pass the split specifications list to the template
        'box_contain':box_contain,
        'categories': categories,'title':'Accu-Mart | Product Detail'
    })
# end

# add to cart start
def add_to_cart(request, pk):
    categories = Category.objects.all()
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'You need to log in first!'}, status=400)

    product = Product.objects.get(pk=pk)

    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False,
    )

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs.first()

        # Check if the product is already in the cart
        if order.items.filter(product__pk=pk).exists():
            message = "This product is already in your cart."
        else:
            order.items.add(order_item)
            message = "Item added to cart"
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        message = "Item added to cart"

    # Return the updated cart information as a JSON response
    item_count = order.items.count()
    total_price = order.get_total_price()
    serialized_categories = serializers.serialize('json', categories)

    return JsonResponse({
        'message': message,
        'item_count': item_count,
        'total_price': total_price,
        # 'categories':categories,
        'categories':serialized_categories,
    })

# Increase the quantity of the product in the cart
def increase_quantity(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'You need to log in first!'}, status=400)

    product = Product.objects.get(pk=pk)
    order_item = OrderItem.objects.get(product=product, user=request.user, ordered=False)

    order_item.quantity += 1
    order_item.save()

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order = order_qs.first()

    item_count = order.items.count()
    total_price = order.get_total_price()

    return JsonResponse({
        'message': "Quantity increased",
        'item_count': item_count,
        'total_price': total_price,
    })

# Decrease the quantity of the product in the cart
def decrease_quantity(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'You need to log in first!'}, status=400)

    # Get the product and the OrderItem
    product = Product.objects.get(pk=pk)
    order_item = OrderItem.objects.get(product=product, user=request.user, ordered=False)

    # Ensure the quantity does not go below 1
    if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.save()

        message = "Quantity decreased"
    else:
        message = "Quantity cannot be less than 1"

    # Get the current order
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order = order_qs.first()

    item_count = order.items.count()
    total_price = order.get_total_price()

    return JsonResponse({
        'message': message,
        'item_count': item_count,
        'total_price': total_price,
    })

# add blog start
def add_blog(request):
    categories = Category.objects.all()
    if request.method == 'POST':
       form = BlogForm(request.POST, request.FILES) 
       if form.is_valid():
            form.save()
            messages.success(request, 'Blog added successfully!')
            return redirect('blog_index')
       else:
           messages.error(request, 'PLEASE CHECK THE FORM.')
           messages.info(request,'Blog IS NOT  ADDED...........')
    #    return redirect('/')
    else:
        form = BlogForm()
    return render(request,'core/blog/add_blog.html',{'form':form,'categories':categories,'title':'Accu-Mart | Add Blog'})
# add blog end
def edit_blog(request, id):
    blog = get_object_or_404(MyBlog, id=id)
    categories=Category.objects.all()
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'blog edited successfully!')
            return redirect('blog', blog.id)
    else:
        form = BlogForm(instance=blog)

    return render(request, 'core/blog/edit_blog.html', {'form': form, 'blog': blog,'categories':categories})

def delete_blog(request, id):
    blog = get_object_or_404(MyBlog, id=id)
    categories = Category.objects.all()
    if request.method == 'POST':
        # print("product deleted")
        blog.delete()
        messages.success(request, 'blog deleted successfully!')
        return redirect('blog_index')  # Redirect to product list after deletion

    return render(request, 'core/blog/blog.html', {'blog': blog,'categories':categories})
def blog_index(request):
    blogs = MyBlog.objects.all().order_by('-blog_post_date')
    categories = Category.objects.all()
     # Set up pagination
    paginator = Paginator(blogs, 6) 
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)

    # return render(request, 'blog_index.html', {'page_obj': page_obj})
    return render(request,'core/blog/blog_index.html',{'blogs':blogs,'page_obj': page_obj,'categories':categories,'title':'Accu-Mart | Blog'})

def blog(request,pk):
    blog = MyBlog.objects.get(pk=pk)
    categories = Category.objects.all()
    return render(request,'core/blog/blog.html',{'blog':blog,'categories':categories,'title':'Accu-Mart | Blog Detail'})

def update_cart_quantity(request, pk):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        action = request.POST.get('action')
        print(f"Action received: {action}")  # Debugging print statement
        order_item = get_object_or_404(OrderItem, pk=pk, user=request.user, ordered=False)

        if action == 'increase':
            # Increase quantity
            order_item.quantity += 1
        elif action == 'decrease':
            if order_item.quantity > 1:
                # Decrease quantity (but prevent going below 1)
                order_item.quantity -= 1
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'You can not decrease the quantity below 1.',
                    'order_item_id': pk,
                })

        # Save the updated quantity
        order_item.save()

        # Recalculate the prices for the order
        order = order_item.user.order_set.filter(ordered=False).first()
        if order:
            order.subtotal_price = order.get_subtotal_price()
            order.total_price = order.get_total_price()
            order.total_gst = order.get_total_gst()
            order.save()

        # Return updated data to update the frontend
        return JsonResponse({
            'success': True,
            'order_item_id': order_item.id,
            'quantity': order_item.quantity,
            'total_price': order_item.product.price * order_item.quantity,
            'subtotal_price': order.subtotal_price,
            'total_price': order.total_price,
            'total_gst': order.total_gst,
            'message': 'Item quantity updated successfully' if order_item.pk else 'Item removed from cart.',
        })

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)



# function for deleting product from cart
def delete_cart_item(request, pk):
    # Ensure it's an AJAX request and POST method
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        order_item = get_object_or_404(OrderItem, pk=pk, user=request.user, ordered=False)

        # Delete the item from the cart
        order_item.delete()

        # Get the updated order and recalculate totals
        order = Order.objects.get(user=request.user, ordered=False)
        subtotal_price = order.get_subtotal_price()
        total_price = order.get_total_price()
        total_gst = order.get_total_gst()
        item_count = order.items.count()
        # Return the updated totals and a success message
        return JsonResponse({
            'success': True,
            'message': 'Item successfully removed from cart.',
            'subtotal_price': subtotal_price,
            'total_price': total_price,
            'total_gst': total_gst,
            'item_count':item_count,
        })

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


# fetch products by category
def fetch_product_cate(request):
    categories = Category.objects.all()
    category_id = request.GET.get('category_id')
    if category_id:
        try:
            category = Category.objects.get(id=category_id)
            products = Product.objects.filter(category=category)
        except Category.DoesNotExist:
            products = Product.objects.all()  # Fallback to showing all products if category doesn't exist
            category = None
    else:
        products = Product.objects.all()
        category = None  # No category selected, so category is None

    return render(request, 'core/products/fetch_products_cat.html', {
        'products': products,
        'category': category,
        'categories': categories,  # Pass all categories to the template
        'title':'Accu-Mart | Products'
    })

# for index page products to redirect if user click on any product
def filter_products(request, category_name):
    categories =Category.objects.all()
    try:
        category = Category.objects.get(category_name=category_name)
    except Category.DoesNotExist:
        raise Http404("Category not found")

    # Filter products based on the category
    products = Product.objects.filter(category=category)

    return render(request, 'core/products/filter_products.html', {'products': products,'category': category,'categories': categories,'title':'Accu-Mart | Products'})

def all_products(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request,'core/products/all_products.html',{'categories':categories,'products':products, 'title':'Accu-Mart | All Products'})

def checkout_page(request):
    orders = Order.objects.filter(user=request.user)

    if not orders.exists():
        messages.error(request, "You don't have any orders.")
        return redirect('index') 

    # Fetch the most recent order (or first if you prefer)
    order = orders.order_by('-ordered_date').first()

    # Fetch categories as usual
    categories = Category.objects.all()

    customer_details = checkoutAddress.objects.filter(user=request.user).last()  # Get the most recent address
   
    # Handle GET request - show customer details and the form
    if request.method == 'GET':
        if customer_details:
            form = CheckoutAddressForm(instance=customer_details)  # Pre-fill the form with existing data
        else:        
             form = CheckoutAddressForm()
        return render(request, 'core/checkout/checkout.html', {
            'order': order,
            'categories': categories,
            'customer_details': customer_details,
            'form': form,  # Pass the form to the template
            'title':'Accu-Mart | Checkout'
        })

    # Handle POST request - user submits the form
    if request.method == 'POST':
        form = CheckoutAddressForm(request.POST)  # Prefill form with existing data
        if form.is_valid():
            # Save the updated form data
            updated_customer_details = form.save(commit=False)
            updated_customer_details.user = request.user  # Ensure the user is set correctly
            updated_customer_details.save() 
            order.checkout_address = updated_customer_details
            order.save()
            # Render the checkout page with updated details
            return render(request, 'core/checkout/checkout.html', {
                'payment_allow': "allow",  # This can be set dynamically based on your payment logic
                'order': order,
                'categories': categories,
                'customer_details': updated_customer_details,
                'title':'Accu-Mart | Checkout'
            })
        else:
            # If the form is not valid, return the form with error messages
            return render(request, 'core/checkout/checkout.html', {
                'form': form,
                'order': order,
                'categories': categories,
                'title':'Accu-Mart | Checkout'
            })

def payment(request):   
    try:
        order =Order.objects.get(user=request.user,ordered=False)
        customer_details = checkoutAddress.objects.get(user=request.user)
        categories = Category.objects.all()
        order_amount=order.get_total_price()
        order_currency ='INR'
        # payment_method = request.POST.get('payment_method')
        # order_receipt = order.order_id
        notes={
            "first_name":customer_details.first_name,
            "last_name":customer_details.last_name,
            "phone":customer_details.phone,
            "email":customer_details.email,
            "city":customer_details.city,
            "state":customer_details.state,
            "country":customer_details.country.name,
            "zip_code":customer_details.zip_code,
        }
        # if payment_method == 'razorpay':
        razorpay_order = razorpay_client.order.create(
                dict(
                    amount=order_amount * 100,
                    currency =order_currency,
                    notes = notes,
                    payment_capture ="0",
                )
            )
        print(razorpay_order["id"])
        order.razorpay_order_id=razorpay_order["id"]
        order.save()
        print("It Should render the summary page...........................")
            
        return render(request,'core/checkout/razorpay_payment_summary.html',{
                "order":order,
                "order_id":razorpay_order["id"],
                "orderId":order.order_id,
                "final_price":order_amount,
                "razorpay_merchant_id":settings.RAZORPAY_ID,
                "customer_details":customer_details,
                'categories':categories,
                'title':'Accu-Mart | Payment'
            })

    except Order.DoesNotExist:
        print("Order Not Found...................................")
        return HttpResponse("404 Error..................")
    

@csrf_exempt
def handlerequest(request):
    if request.method =='POST':
        try:
            categories = Category.objects.all()
            payment_id = request.POST.get('razorpay_payment_id','')
            order_id=request.POST.get('razorpay_order_id','')
            signature=request.POST.get('razorpay_signature','')
            print(payment_id,order_id,signature)
            params_dict={
                'razorpay_payment_id':payment_id,
                'razorpay_order_id':order_id,
                'razorpay_signature':signature,
            }
            try:
                order_db =Order.objects.get(razorpay_order_id=order_id)
                print("order found...................")
            except:
                print("order not found.............")
                return HttpResponse("505 Not Found....")
            order_db.razorpay_payment_id=payment_id
            order_db.razorpay_signature=signature
            order_db.save()
            print("Working..................")
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            print("Result.............",result)
            # if result ==None:
            if result:
                print("Result working final fine................")
                amount = order_db.get_total_price()
                amount = amount * 100
                payment_status = razorpay_client.payment.capture(payment_id,amount)
                if payment_status is not None:
                    print("payment_status",payment_status)
                    order_db.ordered =True
                    order_db.is_paid = True
                    order_db.status = 'Paid'
                    order_db.save()
                    print("Payment Successfull................")
                    
                    request.session[
                        'order_complete'
                    ]="Your Order is Placed Successfully"
                    return render(request,"core/index.html",{'categories':categories})
                    # return render(request,"core/invoice.html")
                else:
                    print("Payment FAiled................")
                    order_db.ordered = False
                    order_db.save()
                    request.session[
                        'order_failed'
                    ]="Your Order could not be placed, please try again"
                    return('/')
            else:
                order_db.ordered =False
                order_db.save()
                return redirect(request,'core/checkout/payment_failed.html')
        except:
            return HttpResponse('Error Found..............................!!!!!!!!!!!!!!')
'''

def generate_hash(key, txnid, amount, productinfo, firstname, email, salt):
     input_str = f"{key}|{txnid}|{amount}|{productinfo}|{firstname}|{email}|||||||||||{salt}"
     return hashlib.sha512(input_str.encode('utf-8')).hexdigest()

def payment(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        customer_details = checkoutAddress.objects.filter(user=request.user).last()
        categories = Category.objects.all()
        order_amount = order.get_total_price()
        order_currency = 'INR'

        # PayU related details
        # payu_merchant_key = settings.PAYU_MERCHANT_KEY
        # payu_merchant_salt = settings.PAYU_MERCHANT_SALT
        # payu_api_url = settings.PAYU_API_URL
        payu_api_url = settings.PAYU_API_URL_TEST
        payu_merchant_key = settings.PAYU_MERCHANT_KEY_TEST
        payu_merchant_salt = settings.PAYU_MERCHANT_SALT_TEST
        payment_method = request.POST.get('payment_method')

        if payment_method == 'razorpay':
            # Razorpay Payment
            razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_ID, settings.RAZORPAY_SECRET))
            razorpay_order = razorpay_client.order.create(dict(
                amount=order_amount * 100,  # Razorpay expects amount in paise
                currency=order_currency,
                payment_capture="0",  # Payment will be captured manually later
            ))

            order.razorpay_order_id = razorpay_order["id"]
            order.save()

            return render(request, 'core/checkout/razorpay_payment_summary.html', {
                "order": order,
                "order_id": razorpay_order["id"],
                "orderId": order.order_id,
                "final_price": order_amount,
                "razorpay_merchant_id": settings.RAZORPAY_ID,
                "customer_details": customer_details,
                'categories': categories,
                'title': 'Accu-Mart | Payment'

              
            })
        


        # payment_method = request.POST.get('payment_method')

        elif payment_method == 'payu':
            # PayU Payment
            payu_order = {
                "key": payu_merchant_key,
                "txnid": order.order_id,
                "amount": order_amount,
                "productinfo": "Order Payment",
                "firstname": customer_details.first_name,
                "email": customer_details.email,
                "phone": customer_details.phone,
                "surl": settings.PAYU_SUCCESS_URL,
                "furl": settings.PAYU_FAILURE_URL,
                "service_provider": "payu_paisa",
            }

            # Calculate the hash using the correct formula
            payu_order["hash"] = generate_hash(
                payu_merchant_key,
                payu_order["txnid"],
                str(payu_order["amount"]),
                payu_order["productinfo"],
                payu_order["firstname"],
                payu_order["email"],
                payu_merchant_salt
            )

            # Save PayU order ID to the Order Model
            order.payu_order_id = payu_order["txnid"]
            order.save()

            return render(request, 'core/checkout/payu_payment_summary.html', {
                "order": order,
                "payu_order": payu_order,
                "order_id": payu_order["txnid"],
                "final_price": order_amount,
                "payu_merchant_key": payu_merchant_key,
                'categories': categories,
                "customer_details": customer_details,
                'title': 'Accu-Mart | Payment'
            })

        else:
            return redirect('payment_failed')
    
    except Order.DoesNotExist:
        print("Order Not Found")
        return HttpResponse("404 Error")

@csrf_exempt
def handlerequest(request):
    if request.method == 'POST':
        try:
            # # Razorpay response handling
            categories = Category.objects.all()
            payment_id = request.POST.get('razorpay_payment_id','')
            order_id=request.POST.get('razorpay_order_id','')
            signature=request.POST.get('razorpay_signature','')
            print(payment_id,order_id,signature)

            
            # PayU response handling
            payu_payment_status = request.POST.get('payment_status', '')
            payu_txnid = request.POST.get('txnid', '')
            payu_signature = request.POST.get('hash', '')

            if payment_id:
                params_dict={
                    'razorpay_payment_id':payment_id,
                    'razorpay_order_id':order_id,
                    'razorpay_signature':signature,
                }
                try:
                    order_db =Order.objects.get(razorpay_order_id=order_id)
                    print("order found...................")
                except:
                    print("order not found.............")
                    return HttpResponse("505 Not Found....")
                order_db.razorpay_payment_id=payment_id
                order_db.razorpay_signature=signature
                order_db.save()
                print("Working..................")
                result = razorpay_client.utility.verify_payment_signature(params_dict)
                print("Result.............",result)
                # if result ==None:
                if result:
                    print("Result working final fine................")
                    amount = order_db.get_total_price()
                    amount = amount * 100
                    payment_status = razorpay_client.payment.capture(payment_id,amount)
                    if payment_status:
                        print("payment_status",payment_status)
                        order_db.ordered =True
                        order_db.is_paid = True
                        order_db.status = 'Paid'
                        order_db.save()
                        print("Payment Successfull................")
                        request.session[
                            'order_complete'
                        ]="Your Order is Placed Successfully"
                        return render(request,"core/checkout/payment_success.html",{'categories':categories,'payment_status':payment_status,'order':order_db})
                        # return render(request,"core/invoice.html")
                    else:
                        print("Payment FAiled................")
                        order_db.ordered = False
                        order_db.is_paid = False
                        order_db.status = 'Pending'
                        order_db.save()
                        request.session[
                            'order_failed'
                        ]="Your Order could not be placed, please try again"
                        return render('payment_failure')
                else:
                    order_db.ordered =False
                    order_db.is_paid = False
                    order_db.status = 'Pending'
                    order_db.save()
                    return redirect(request,'core/checkout/razorpay_payment_summary.html')


            # Verify PayU signature
            elif payu_payment_status:
                hash_string = f"{settings.PAYU_MERCHANT_KEY}|{payu_txnid}|{order_id.get_total_price()}|Order Payment|{order_id.user.email}|{payu_payment_status}|{payu_txnid}|{payu_signature}"
                payu_verified_hash = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
                if payu_verified_hash == payu_signature:
                    order_id.ordered = True if payu_payment_status == "success" else False
                    order_id.save()
                    return redirect('/')
                else:
                    return redirect(request,'core/checkout/payu_payment_summary.html')

        except Exception as e:
            print(f"Error Found: {str(e)}")
            return HttpResponse('Error Found')
    return HttpResponse('Invalid request method')



'''

def payment_failure(request):
    return render(request, 'core/checkout/payment_failure.html', {
        'message': 'Sorry, there was an issue with your payment. Please try again.'
    })

def payment_success(request):
    return render(request, 'core/checkout/payment_success.html', {
        'message': 'Your payment was successful! Thank you for your order.'
    })

def validate_phone(phone):
    # Example regex pattern for validating phone numbers (can be adjusted for specific formats)
    pattern = r'^\+91[\s\-]?[7-9][0-9]{9}$|^[7-9][0-9]{9}$'

# This allows for an optional "+" and requires a 9 to 15 digit phone number
    if not re.match(pattern, phone):
        raise ValidationError("Invalid phone number format. Please enter a valid phone number.")


# function for genrating call request
def request_call(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        time = request.POST.get('time')
        user_email = request.POST.get('email')

        # Validate the user's email address
        try:
            validate_email(user_email) 
        except ValidationError:
            return JsonResponse({'message': 'Invalid email address. Please enter a valid email.'}, status=400)

        # Validate the phone number
        try:
            validate_phone(phone) 
        except ValidationError:
            return JsonResponse({'message': 'Invalid phone number format. Please enter a valid phone number.'}, status=400)

        # Compose the email for the admin
        subject_to_admin = f"Request a Call from {name}"
        body_to_admin = render_to_string('core/emails/admin_request_call.html', {
            'name': name,
            'phone': phone,
            'email': user_email,
            'time': time,
        })

        # Send email to admin from the user's email
        try:
            send_mail(
                subject_to_admin,  # Subject of the email
                '',  # No plain text body, sending HTML
                user_email,  # From email (user's email)
                [settings.DEFAULT_FROM_EMAIL],  # To email (admin's email)
                fail_silently=False,
                html_message=body_to_admin  # Send HTML formatted body
            )

            # Send a thank you email to the user
            subject_to_user = "Thank you for requesting a call!"
            body_to_user = render_to_string('core/emails/user_thank_you_request.html', {
                'name': name,
                'phone': phone,
                'time': time,
            })

            send_mail(
                subject_to_user,  # Subject of the email
                '',  # No plain text body
                settings.DEFAULT_FROM_EMAIL,  # From email (default from email)
                [user_email],  # To the user's email
                fail_silently=False,
                html_message=body_to_user  # Send HTML formatted body
            )

            # Return success response to the client (user)
            return JsonResponse({'message': 'Your request has been submitted successfully! We will contact you soon.'}, status=200)

        except Exception as e:
            # If there's any error, return an error message
            return JsonResponse({'message': f'Failed to send the message. Error: {str(e)}'}, status=500)

    # If method is not POST, return an error message
    return JsonResponse({'message': 'Invalid request method. Please submit the form using the correct method.'}, status=400)

def contact_us(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            try:
                # Prepare the HTML email content for the admin
                admin_email_subject = f"New message from {name} - {subject}"
                admin_email_body = render_to_string('core/emails/admin_message.html', {
                    'name': name,
                    'email': email,
                    'subject': subject,
                    'message': message,
                })

                # Send email to admin
                send_mail(
                    admin_email_subject,
                    '',  # No plain text body, as we are sending HTML
                    email,  # From the user's email
                    [settings.DEFAULT_FROM_EMAIL],  # Admin email
                    fail_silently=False,
                    html_message=admin_email_body  # Send the HTML formatted body
                )
                
                # Prepare the thank-you email content for the user
                user_email_subject = "Thank you for your message"
                user_email_body = render_to_string('core/emails/user_thank_you.html', {
                    'name': name,
                    'subject': subject,
                    'message': message,
                })

                # Send thank you email to user
                send_mail(
                    user_email_subject,
                    '',  # No plain text body
                    settings.DEFAULT_FROM_EMAIL,  # From the default email
                    [email],  # To the user's email
                    fail_silently=False,
                    html_message=user_email_body  # Send the HTML formatted body
                )

                # Show success message and redirect
                messages.success(request, "Thank you for your message. We will get back to you shortly.")
                return redirect('contact_us')

            except Exception as e:
                messages.error(request, f"An error occurred while sending your message: {str(e)}")
                return redirect('contact_us')

        else:
            # If form is not valid, display errors
            messages.error(request, "There were some errors in your form submission. Please check and try again.")
            return render(request, 'core/contact_us.html', {'form': form,'categories':categories})

    else:
        form = ContactForm()
    return render(request, 'core/contact_us.html', {'form': form,'categories':categories,'title':'Accu-Mart | Contact Us'})


@login_required
def add_to_wishlist(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
        wishlist_item_count= Wishlist.objects.filter(user=request.user).count()
        if created:
            message = "Product added to wishlist"
            
        else:
            message = "Product already in wishlist"

        return JsonResponse({
            'status': 'success',
            'message': message,
            'wishlist_item_count': wishlist_item_count,
        })
    except Product.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)
    

def view_wishlist(request):
    # Get the user's wishlist items
    wishlist_items = Wishlist.objects.filter(user=request.user)
    wishlist_count = wishlist_items.count()
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'core/wishlist/view_wishlist.html', {
        'wishlist_items': wishlist_items,
        'wishlist_count': wishlist_count,
        'categories':categories,
        'products':products,
        'title':'Accu-Mart | Wishlist'
    })



@login_required
def remove_from_wishlist(request, product_id):
    if request.method == 'POST':
        try:
            wishlist_item = Wishlist.objects.get(user=request.user, product_id=product_id)

            wishlist_item.delete()

            wishlist_item_count = Wishlist.objects.filter(user=request.user).count()

            return JsonResponse({
                'message': 'Product removed from wishlist',
                'wishlist_item_count': wishlist_item_count,
                'removed_product': True  ,
            })

        except Wishlist.DoesNotExist:
            # If no wishlist entry is found
            return JsonResponse({
                'message': 'Product not found in wishlist',
                'wishlist_item_count': 0,
                'removed_product': False
            })

        except Exception as e:
            return JsonResponse({
                'message': f'An error occurred: {str(e)}',
                'wishlist_item_count': 0,
                'removed_product': False
            })

    return JsonResponse({
        'message': 'Invalid request method',
        'wishlist_item_count': 0,
        'removed_product': False
    })




def product_search(request):
    # Get the query from the GET request (default to an empty string)
    query = request.GET.get('query', '').strip()
    categories = Category.objects.all()
    products = Product.objects.all()

    # If there is a query, filter the products by Product_Name
    if query:
        # Case-insensitive search for Product_Name using 'icontains'
        products = products.filter(Product_Name__icontains=query)
    
    # Pass the query and filtered products to the template
    return render(request, 'core/products/product_search.html', {
        'query': query,
        'products': products,
        'categories':categories
    })

def order_detail(request):
    # Fetch orders for the logged-in user along with the associated checkout address and order items
    orders = Order.objects.all().order_by('-ordered_date').prefetch_related('checkout_address','items__product')
    print(".....................................",orders)
    # Categories for the sidebar or navigation
    categories = Category.objects.all()

    # Prepare context data
    context = {
        'orders': orders,
        'categories': categories,
    }

    return render(request, 'core/order/order_list.html', context)


