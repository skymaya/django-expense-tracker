from datetime import datetime
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.signals import user_logged_out, user_login_failed
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.db.models import Sum
from .forms import SignUpForm, ExpenseForm
from .models import Expense, ExpenseCategory
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import DetailView


def logout_message(sender, user, request, **kwargs):
    messages.success(request, '<i class="bi bi-check-circle-fill"></i> You have been successfully logged out.')

def login_failed_message(sender, credentials, request, **kwargs):
    messages.error(request, '<i class="bi bi-x-circle-fill"></i> Login failed.')

user_logged_out.connect(logout_message)
user_login_failed.connect(login_failed_message)


class LoggedInTemplateView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = None


class LoggedInDetailView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = None


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


class DashboardView(LoggedInView):
    template_name = "members/dashboard.html"
    expense_model = Expense

    def get(self, request, *args, **kwargs):

        this_month = datetime.now().month
        this_year = datetime.now().year
        user_expense_data = self.expense_model.objects.filter(
            user=request.user,
            date__month=this_month,
            date__year=this_year
        )
        data = {
            'user_data': user_expense_data,
            'amount_sum': user_expense_data.aggregate(Sum('amount'))['amount__sum'],
        }
        return render(request, self.template_name, data)


class ExpenseCategoryView(LoggedInView):
    template_name = "members/expense_category.html"
    form_class = ExpenseForm
    expense_model = Expense
    category_model = ExpenseCategory

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        submit_val = request.POST.get('submit')

        category = self.category_model.objects.get(slug=self.kwargs['slug'])

        if submit_val == 'add':
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = request.user
                obj.category = category
                obj.save()
                messages.success(request, 'Expense added')
            else:
                messages.error(request, 'Expense add failed')

        if submit_val == 'delete':
            obj_pk = request.POST.get('delete_pk')
            try:
                obj = self.expense_model.objects.get(
                    user=request.user,
                    pk=obj_pk
                )
            except ObjectDoesNotExist:
                messages.error(request, 'Delete failed')
            else:
                obj.delete()
                messages.success(request, 'Expense deleted')

        return HttpResponseRedirect(self.request.path_info)

    def get(self, request, *args, **kwargs):

        category = get_object_or_404(
            self.category_model,
            slug__iexact=self.kwargs['slug']
        )

        add_expense_form = self.form_class()
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
            'add_expense_form': add_expense_form,
            'amount_sum': user_expense_data.aggregate(Sum('amount'))['amount__sum'],
            'category_name': category.name,
            'category_description': category.long_description
        }
        return render(request, self.template_name, data)
