from django import template

register = template.Library()

@register.filter
def isinstanceof(value, class_name):
    try:
        class_obj = value.__class__
        return class_obj.__module__ + '.' + class_obj.__qualname__ == class_name
    except AttributeError:
        return False
