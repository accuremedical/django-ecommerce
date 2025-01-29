# templatetags/form_filters.py

from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, class_name):
    """
    Adds the given class to the field's widget.attrs['class'].
    """
    # Check if the field has a widget and then add the class
    if hasattr(field, 'widget'):
        current_classes = field.widget.attrs.get('class', '')
        # Add the new class to the existing ones, if any
        if current_classes:
            field.widget.attrs['class'] = f"{current_classes} {class_name}"
        else:
            field.widget.attrs['class'] = class_name
    return field
