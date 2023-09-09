from django.urls import path
from .views import SignUpView, DashboardView, CustomLoginView, ExpenseCategoryView, logout_view

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("logout/", logout_view, name="logout"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("<slug:slug>/", ExpenseCategoryView.as_view(), name="expense_category"),
]