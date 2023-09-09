from django.urls import path

from main.views import HomeView, PrivacyPolicyView

urlpatterns = [
    # do not include a / for this view as it breaks things
    path("", HomeView.as_view(), name="home"),
    path("privacy", PrivacyPolicyView.as_view(), name="privacy"),
]