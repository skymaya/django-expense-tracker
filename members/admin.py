from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import ExpenseCategoryForm
from .models import (
    User, 
    ExpenseCategory, 
    SupportTicket,
    SupportTicketReply
)


class CategoryAdmin(admin.ModelAdmin):
    form = ExpenseCategoryForm


class SupportTicketReplyInline(admin.StackedInline):
    model = SupportTicketReply
    extra = 1  # Number of empty forms to display


class SupportTicketAdmin(admin.ModelAdmin):
    inlines = [SupportTicketReplyInline]


admin.site.register(User, UserAdmin)
admin.site.register(ExpenseCategory, CategoryAdmin)
admin.site.register(SupportTicket, SupportTicketAdmin)
