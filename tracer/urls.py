from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve

from mysite import settings
from tracer.views import account


urlpatterns = [
    path('register/', account.register, name='register'),
    path('register_valid_code/', account.register_valid_code),
    path('login/', account.login, name='login'),
    path('login/sms/', account.login_sms, name='login_sms'),
    path('get_validCode_img/', account.get_validCode_img, name='image_code'),
    path('index/', account.index, name='index'),
    re_path('^$', account.index),
    path('logout/', account.logout),
    re_path(r"media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    # path('upload/', account.upload),

]