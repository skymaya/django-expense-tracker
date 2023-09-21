from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("main.urls")),
    path("", include("django.contrib.auth.urls")),
]
