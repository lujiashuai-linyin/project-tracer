from django.contrib import admin
from django.urls import path, re_path, include
from tracer.views import account


urlpatterns = [
    path('register/', account.register, name='register'),
    path('register_valid_code/', account.register_valid_code),
    path('login/', account.login, name='login'),
    path('login/sms/', account.login_sms, name='login_sms'),
    path('get_validCode_img/', account.get_validCode_img, name='image_code'),
    path('index/', account.index),
    re_path('^$', account.index),

]