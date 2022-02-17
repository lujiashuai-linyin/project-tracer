from django.contrib import admin
from django.urls import path, re_path, include
from tracer.views import account


urlpatterns = [
    path('register/', account.register),
    path('register_valid_code/', account.register_valid_code),
    path('login/', account.login),
    # re_path('^$', views.index),

]