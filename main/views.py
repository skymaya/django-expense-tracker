from django.views.generic import TemplateView
from django.contrib import messages


class HomeView(TemplateView):
    template_name = "main/home.html"


class PrivacyPolicyView(TemplateView):
    template_name = "main/privacy.html"
