from django.conf import settings
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django_countries.fields import CountryField # type: ignore
from django.core.validators import RegexValidator
from django.contrib import admin

# Create your models here.

class Customer(models.Model):

    user = models.OneToOneField(User,null=False,blank=False,on_delete=models.CASCADE)

    #extra fields come here
    phone_field =models.CharField(max_length=12,blank=False,null=False)
    email =models.EmailField(max_length=100,blank=True,null=False)
    def __str__(self):
        return self.user.username
    
#Category model where different Categories will be stored
class Category(models.Model):
    category_name = models.CharField(max_length=200)
    def __str__(self):
        return self.category_name
    
class Product(models.Model):
    Product_Name=models.CharField(max_length=100)
    category=models.ForeignKey('Category',on_delete=models.CASCADE)
    desc = models.TextField()
    features =models.TextField(help_text="Enter each feature on a new line.",blank=True,null=True)
    specifications =models.TextField(help_text="Enter each specification on a new line.",blank=True,null=True)
    box_contain =models.TextField(blank=True,null=True)
    price = models.FloatField(default=0.0)
    gst_percentage = models.FloatField(
        choices=[(5.00, '5%'), (12.00, '12%'), (18.00, '18%')],
        default=18.00
    )
    hsn_code =models.CharField(max_length=20,blank=True,null=True)
    img = models.ImageField(upload_to='images/')
    product_catelog = models.FileField(upload_to='catelogs/',blank=True,null=True)

    def get_add_to_cart_url(self):
       return reverse("core:add-to-cart", kwargs={'pk':self.pk})

    def __str__(self):
      return self.Product_Name
    


# product model end

 # blog model start
class MyBlog(models.Model):
    blog_title=models.CharField(max_length=500)
    blog_desc_1 = models.TextField()
    blog_heading_1=models.CharField(max_length=500,blank=True,null=True)
    blog_desc_2 = models.TextField(blank=True,null=True)
    blog_heading_2=models.CharField(max_length=500,blank=True,null=True)
    blog_desc_3 = models.TextField(blank=True,null=True)

    blog_heading_3=models.CharField(max_length=500,blank=True,null=True)
    blog_desc_4 = models.TextField(blank=True,null=True)
    blog_heading_4=models.CharField(max_length=500,blank=True,null=True)
    blog_desc_5 = models.TextField(blank=True,null=True)
    blog_conclusion_h=models.CharField(max_length=500,blank=True,null=True)
    blog_desc_conc = models.TextField(blank=True,null=True)
   
    img_1 = models.ImageField(upload_to='blog/')
    img_2 = models.ImageField(upload_to='blog/',blank=True,null=True)
    blog_post_date =models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
      return self.blog_title
 # blog model end  

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.Product_Name}"
    
    def get_total_item_price(self):
        return self.quantity * self.product.price
    
    # def get_final_price(self):
    #     return self.get_total_item_price()
    
    def get_final_price(self):
        # Assuming this method returns the base price (price before tax)
        base_price = self.product.price * self.quantity
        gst_percentage = self.product.gst_percentage
        gst_amount = (base_price * gst_percentage) / 100  # Calculating GST
        final_price = base_price + gst_amount  # Total price including GST
        return final_price
    
# class for Checkout

class checkoutAddress(models.Model):    
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key to User
    first_name = models.CharField(max_length=100,  null=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(null=True, blank=False,max_length=10)  # Using PhoneNumberField to store phone 
    email =models.CharField(max_length=100 ,null=True)
    address = models.CharField(max_length=250, null=True, blank=False)
    city = models.CharField(max_length=100, null=True, blank=False)
    state = models.CharField(max_length=100, null=True, blank=False)

    country = CountryField(multiple=False, blank_label='(Select country)', default='IN', null=True, blank=True)  # Using CountryField for selecting a country
    zip_code =models.CharField(max_length=20, null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.user.username

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date =models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default = False)
    order_id = models.CharField(max_length=100,unique=True,default=None,blank=True,null=True)
    datetime_ofpayment = models.DateTimeField(auto_now_add=True)
    order_delivered = models.BooleanField(default=False)
    order_received = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=50, default='Pending')
    checkout_address = models.ForeignKey(checkoutAddress, on_delete=models.SET_NULL, null=True, blank=True)
    razorpay_order_id = models.CharField(max_length=500,null=True,blank=True)
    razorpay_payment_id = models.CharField(max_length=500,null=True,blank=True)
    razorpay_signature = models.CharField(max_length=500,null=True,blank=True)


    def save(self,*args, **kwargs):
        if self.order_id is None and self.datetime_ofpayment and self.id:
            self.order_id = self.datetime_ofpayment.strftime('PAY2ME%Y%m%dODR')+ str(self.id)

        return super().save( *args, **kwargs)
    


    def __str__(self):
        return self.user.username
    
    def get_subtotal_price(self):
        sub_total =0
        for order_item in self.items.all():
            sub_total+= order_item.get_total_item_price() # excluding gst
        return round(sub_total, 2)

    def get_total_price(self):
            total = 0
            for order_item in self.items.all():
                total += order_item.get_final_price()  # This includes GST
            return round(total, 2)
    
      # function for calculating gst amount
    def get_total_gst(self):
        total_gst = 0
        for order_item in self.items.all():
            base_price = order_item.product.price * order_item.quantity
            gst_percentage = order_item.product.gst_percentage
            gst_amount = (base_price * gst_percentage) / 100
            total_gst += gst_amount
        return round(total_gst,2)
    
    # calculating shipping & Delivery charges
    # def get_shipping_gst
    
    def get_total_count(self):
        order =Order.objects.get(pk=self.pk)
        return order.items.count()

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # Ensure one product per user only

    def __str__(self):
        return f'{self.user.username} - {self.product.Product_Name}'

   