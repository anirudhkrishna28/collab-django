from django.contrib import admin
from django.urls import path
from codechat.views import index
from codechat.api_views import register,login

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
     path("api/register", register),
    path("api/login", login),
]