from django.contrib import admin
from django.urls import path
from codechat.views import index

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
]