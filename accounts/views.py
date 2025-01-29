from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from core.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import re
from django.conf import settings
from django.core.mail import send_mail
from core.models import Category
# Create your views here.

# user login
def user_login(request):
    categories = Category.objects.all()
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/',{'categories':categories})
        else:
            messages.info(request,'Login Failed, PLease check your credentials!')

    return render(request,'accounts/sign-in.html',{'categories':categories,'title':'Accu-Mart | Sign In'})

# user register / sign-up
'''
def user_register(request):
    if request.method == "POST":
        username = request.POST.get('username') #id you take username 
        email = request.POST.get('email') 
        phone_field = request.POST.get('phone number')
        password = request.POST.get('password')
        confirm_password =request.POST.get('confirm_password')
        # print("POST Data:", request.POST)
        if password == confirm_password:
            
            # print(username,phone,email,password,confirm_password)
            if User.objects.filter(username = username).exists():
                messages.info(request,'User Name already exists!')
                # print('USERAME ALREADY EXISTS.......................')
                return redirect('user_register')
            else:
                if User.objects.filter(email=email).exists():
                    # print('EMAIL ALREADY EXISTS.......................')
                    messages.info(request,'Email already exists!')
                    return redirect('user_register')
                else:
                    user = User.objects.create_user(username=username,email=email,password =password)
                    # print(user)
                    user.save()
                    # print(user,"User..........................................",phone_field)

                    data = Customer(user=user, phone_field=phone_field)
                    # print(data)
                    data.save()
        
                # code for login user will come here
                our_user = authenticate(username=username,password=password) 
                # print(our_user)
                if our_user is not None:
                    login(request,user)
                    # print(our_user)
                    return redirect('/')
        else:
            messages.info(request,'please enter the same password!')
    else:
        # print('Error password and confirm password not matches....')
       redirect('user_register')

    return render(request,'accounts/sign-up.html')
'''


def validate_email_format(email):
    # Regular expression for validating an email address
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)

def send_welcome_email(email, username):
    subject = "Welcome to Accu-Mart.com"
    message = f"""
    Dear {username},

    Congratulations! Your account has been successfully created at accu-mart.com. 

    We are excited to have you on board! You can now log in and explore our services.

    If you need any assistance or have any questions, feel free to reach out to our support team at info@accuremedical.in or visit our Company.

    Best regards,
    The Accu-Mart Team
    """

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )

def user_register(request):
    categories = Category.objects.all()
    if request.method == "POST":
        username = request.POST.get('username') 
        email = request.POST.get('email') 
        phone_field = request.POST.get('phone number') 
        password = request.POST.get('password')  
        confirm_password = request.POST.get('confirm_password') 

        if password == confirm_password:
            # Validate email format using regex
            if not validate_email_format(email):
                messages.info(request, 'Please enter a valid email address.')
                return redirect('user_register',{'categories':categories,'title':'Accu-Mart | Sign Up'})

            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists!')
                return redirect('user_register',{'categories':categories,'title':'Accu-Mart | Sign Up'})
            # Check if the email already exists
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists!')
                return redirect('user_register',{'categories':categories,'title':'Accu-Mart | Sign Up'})
            else:

                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                data = Customer(user=user, phone_field=phone_field)
                data.save()

                # Send welcome email
                send_welcome_email(email, username)

                our_user = authenticate(username=username, password=password)
                if our_user is not None:
                    login(request, user)
                    return redirect('/',{'categories':categories})

        else:
            messages.info(request, 'Passwords do not match!')

    return render(request, 'accounts/sign-up.html',{'categories':categories,'title':'Accu-Mart | Sign Up'})

# user log-out
def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect('/')
    # Log out the user even if they do a GET request.
    logout(request)  
    return redirect('/') 


