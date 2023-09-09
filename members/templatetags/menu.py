"""docstring"""

from django import template
from members.models import ExpenseCategory

register = template.Library()

@register.simple_tag(name='categories')
def get_categories():
    return ExpenseCategory.objects.all()
