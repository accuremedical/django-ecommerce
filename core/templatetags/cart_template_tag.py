from django import template
from core.models import Order, Wishlist

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user =user, ordered =False)
        if qs.exists():
            # return qs.first().items.count()
            return qs.first().items.count()
    return 0    

@register.filter
def wishlist_item_count(user):
    if user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=user)
        return wishlist_items.count()
    return 0

@register.filter
def get_item(dictionary, key):
    """Retrieve the value from the dictionary for a given key."""
    return dictionary.get(key)