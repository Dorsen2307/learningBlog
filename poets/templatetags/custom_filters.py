from django import template

register = template.Library()

@register.filter
def get(dictionary, key):
    """Возвращает значение по ключу из словаря, если ключ отсутствует, возвращает None."""
    return dictionary.get(key)