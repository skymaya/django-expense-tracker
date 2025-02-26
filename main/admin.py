from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import ExpenseCategoryForm
from .models import (
    User, 
    ExpenseCategory
)


class CategoryAdmin(admin.ModelAdmin):
    form = ExpenseCategoryForm


admin.site.register(User, UserAdmin)
admin.site.register(ExpenseCategory, CategoryAdmin)
