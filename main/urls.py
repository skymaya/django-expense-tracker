from django.urls import path
from .views import (
    SignUpView, 
    DashboardView, 
    LoginView, 
    ExpenseCategoryView, 
    LogoutView, 
    AccountView,
    HomeView
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    #path("privacy", PrivacyPolicyView.as_view(), name="privacy"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("login/", LoginView.as_view(redirect_authenticated_user=True), name="login"),
    path("account/", AccountView.as_view(), name="account"),
    path("<slug:slug>/", ExpenseCategoryView.as_view(), name="expense_category"),
]