from datetime import datetime
import json
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.signals import user_logged_out, user_login_failed
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views import generic, View
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from .forms import (
    SignUpForm, 
    ExpenseForm, 
    TicketForm
)
from .models import (
    Expense, 
    ExpenseCategory, 
    SupportTicket, 
    SupportTicketReply
)


def logout_message(sender, user, request, **kwargs):
    messages.success(request, '<i class="bi bi-check-circle-fill"></i> You have been successfully logged out.')

def login_failed_message(sender, credentials, request, **kwargs):
    messages.error(request, '<i class="bi bi-x-circle-fill"></i> Login failed.')

user_logged_out.connect(logout_message)
user_login_failed.connect(login_failed_message)


class LoggedInView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = None


class LoginView(auth_views.LoginView):
    form_class = AuthenticationForm
    template_name = "members/login.html"


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')


class SignUpView(SuccessMessageMixin, generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "members/signup.html"
    success_message = '<i class="bi bi-check-circle-fill"></i> Signup complete. You may now log in.'


class SupportView(LoggedInView):
    template_name = "members/support.html"
    ticket_model = SupportTicket
    form_class = TicketForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.status = 'Open'
            obj.save()
            messages.success(request, 'Support ticket created')
        else:
            messages.error(request, f'Support ticket create failed{form.errors}')

        return HttpResponseRedirect(self.request.path_info)

    def get(self, request, *args, **kwargs):
        user_tickets = self.ticket_model.objects.filter(user=request.user)
        data = {
            'new_ticket_form': self.form_class(),
            'user_tickets': user_tickets
        }
        return render(request, self.template_name, data)
    

class TicketView(LoggedInView):
    template_name = "members/ticket.html"
    ticket_model = SupportTicket

    def post(self, request, *args, **kwargs):
        # form = self.form_class(request.POST)
        # if form.is_valid():
        #     obj = form.save(commit=False)
        #     obj.user = request.user
        #     obj.status = 'Open'
        #     obj.save()
        #     messages.success(request, 'Support ticket created')
        # else:
        #     messages.error(request, f'Support ticket create failed{form.errors}')

        return HttpResponseRedirect(self.request.path_info)

    def get(self, request, *args, **kwargs):
        ticket = get_object_or_404(
            self.ticket_model,
            pk=self.kwargs['pk'],
            user=request.user
        )
        data = {
            'blah': 'blah',
            'ticket': ticket
        }
        return render(request, self.template_name, data)


class DashboardView(LoggedInView):
    template_name = "members/dashboard.html"
    expense_model = Expense

    def get(self, request, *args, **kwargs):

        this_month = datetime.now().month
        this_year = datetime.now().year

        amount_sum = 0

        result = self.expense_model.objects.filter(
            user=request.user,
            date__month=this_month,
            date__year=this_year
        )\
        .values('category__name', 'category__hex_color')\
        .annotate(total_amount=Sum('amount'))\
        .order_by('total_amount')

        labels = []
        expenses = []
        hex_colors = []

        if result:
            for category in result:
                amount_sum += category['total_amount']
                labels.append(category['category__name'])
                expenses.append(category['total_amount'])
                hex_colors.append(category['category__hex_color'])

        expense_data = {'labels': labels, 'data': expenses, 'hex_colors': hex_colors}

        data = {
            'amount_sum': amount_sum,
            'expense_data_json': json.dumps(expense_data)
        }
        return render(request, self.template_name, data)


class ExpenseCategoryView(LoggedInView):
    template_name = "members/expense_category.html"
    form_class = ExpenseForm
    expense_model = Expense
    category_model = ExpenseCategory

    def post(self, request, *args, **kwargs):
        submit_val = request.POST.get('submit')

        category = self.category_model.objects.get(slug=self.kwargs['slug'])

        if submit_val == 'add':
            form = self.form_class(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = request.user
                obj.category = category
                obj.save()
                messages.success(request, 'Expense added')
            else:
                messages.error(request, f'Expense add failed{form.errors}')

        if submit_val == 'delete':
            obj_pk = request.POST.get('delete_pk')
            try:
                obj = self.expense_model.objects.get(
                    user=request.user,
                    pk=obj_pk
                )
            except ObjectDoesNotExist:
                messages.error(request, 'Expense delete failed')
            else:
                obj.delete()
                messages.success(request, 'Expense deleted')

        if submit_val == 'edit':
            try:
                check_obj = self.expense_model.objects.get(
                    user=request.user,
                    pk=request.POST.get('edit_pk')
                )
                form = self.form_class(request.POST, instance=check_obj)
            except ObjectDoesNotExist:
                messages.error(request, 'Expense update failed')
            else:
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.user = request.user
                    obj.category = category
                    obj.save()
                    messages.success(request, 'Expense updated')
                else:
                    messages.error(request, f'Expense update failed{form.errors}')

        return HttpResponseRedirect(self.request.path_info)

    def get(self, request, *args, **kwargs):

        category = get_object_or_404(
            self.category_model,
            slug__iexact=self.kwargs['slug']
        )

        this_month = datetime.now().month
        this_year = datetime.now().year
        user_expense_data = self.expense_model.objects.filter(
            user=request.user,
            date__month=this_month,
            date__year=this_year,
            category=category
        )
        data = {
            'user_data': user_expense_data,
            'expense_form_edit': self.form_class(),
            'expense_form_add': self.form_class(),
            'amount_sum': user_expense_data.aggregate(Sum('amount'))['amount__sum'],
            'category_name': category.name,
            'category_description': category.long_description
        }
        return render(request, self.template_name, data)
