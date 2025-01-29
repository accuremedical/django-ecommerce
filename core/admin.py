from django.contrib import admin

# Register your models here.
from core.models import Category, Customer, Order, OrderItem, Product, MyBlog,checkoutAddress

# Register your models here.
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(checkoutAddress)
admin.site.register(MyBlog)