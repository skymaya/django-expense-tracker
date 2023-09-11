from django.urls import path
from .views import (
    SignUpView, 
    DashboardView, 
    LoginView, 
    ExpenseCategoryView, 
    LogoutView, 
    SupportView,
    TicketView
)

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("login/", LoginView.as_view(), name="login"),
    path("support/", SupportView.as_view(), name="support"),
    path("ticket/<int:pk>", TicketView.as_view(), name="ticket"),
    path("<slug:slug>/", ExpenseCategoryView.as_view(), name="expense_category"),
]