from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve

from mysite import settings
from tracer.views import account
from tracer.views import project

urlpatterns = [
    path('register/', account.register, name='register'),
    path('register_valid_code/', account.register_valid_code),
    path('login/', account.login, name='login'),
    path('login/sms/', account.login_sms, name='login_sms'),
    path('get_validCode_img/', account.get_validCode_img, name='image_code'),
    path('index/', account.index, name='index'),
    re_path('^$', account.index),
    path('logout/', account.logout, name='logout'),
    re_path(r"media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    # path('upload/', account.upload),
    #项目列表
    path('project/list/', project.project_list, name='project_list'),
    # /project/star/my/1
    # /project/star/join/1
    re_path(r'^project/unstar/(?P<project_type>\w+)/(?P<project_id>\d+)/$', project.project_unstar, name='project_unstar'),
    re_path(r'^project/star/(?P<project_type>\w+)/(?P<project_id>\d+)/$', project.project_star, name='project_star')

]