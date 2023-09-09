from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("members/", include("members.urls")),
    path("members/", include("django.contrib.auth.urls")),
    path("", include("main.urls")),
]
