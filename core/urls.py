from django.urls import path
from core import views

urlpatterns = [


    path('',views.index,name='index'),
    path('add-product',views.add_product,name='add_product'),
    path('product/edit/<int:id>/', views.edit_product, name='edit_product'),
    path('product/delete/<int:id>/', views.delete_product, name='delete_product'),
    path('certification',views.certification,name='certification'),

    path('terms-and-conditions',views.terms_and_conditions,name='terms_and_conditions'),
    path('refund-policy',views.refund_policy,name='refund_policy'),
    path('shipping-policy',views.shipping_policy,name='shipping_policy'),
    path('disclaimer',views.disclaimer,name='disclaimer'),
    path('products',views.fetch_product_cate,name='fetch_product_cate'),
    path('product-description/<pk>',views.product_desc, name = "product_desc"),

     path('increase-quantity/<int:pk>/', views.increase_quantity, name='increase_quantity'),
    path('decrease-quantity/<int:pk>/', views.decrease_quantity, name='decrease_quantity'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('view-cart',views.view_cart,name="view_cart"),
    path('update_cart', views.update_cart, name='update_cart'),

    path('about',views.about,name='about'),

    path('checkout',views.checkout_page,name="checkout_page"),

    path('add-blog',views.add_blog,name='add_blog'),
    
    path('blog/edit/<int:id>/', views.edit_blog, name='edit_blog'),
    path('blog/delete/<int:id>/', views.delete_blog, name='delete_blog'),
    path('blog-index',views.blog_index,name='blog_index'),
    path('blog/<pk>',views.blog,name='blog'),
    
    path('contact/', views.contact_us, name='contact_us'),

     path('filter_products/<str:category_name>/', views.filter_products, name='filter_products'),
     path('all-products',views.all_products,name="all_products"),
     path('payment',views.payment,name='payment'),
     path('response',views.handlerequest,name='handlerequest'),

     path('request-call/', views.request_call, name='request_call'),
     path('update-cart-quantity/<int:pk>/', views.update_cart_quantity, name='update_cart_quantity'),
     path('delete-cart-item/<int:pk>/', views.delete_cart_item, name='delete_cart_item'),

     path('add-to-wishlist/<int:pk>/', views.add_to_wishlist, name='add_to_wishlist'),
     path('view-wishlist/', views.view_wishlist, name='view_wishlist'),
     path('remove-from-wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
     path('search/', views.product_search, name='product_search'),
     path('payment_success', views.payment_success, name='payment_success'),
     path('payment_failure', views.payment_failure, name='payment_failure'),

     path('order/order-list',views.order_detail,name="order_detail"),   
]
