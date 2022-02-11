"""Myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from blog import views
from django.views.static import serve
from Myblog import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('index/', views.index),
    path('logout/', views.logout),
    path('register/', views.register),
    path('get_validCode_img/', views.get_validCode_img),
    re_path('^$', views.index),
    path('upload/', views.upload),

    #后台管理url
    re_path('my_backend/$', views.my_backend),
    re_path("my_backend/add_article/$", views.add_article),

    #点赞
    path("digg/", views.digg),

    #评论
    path("comment/", views.comment),
    path("get_comment_tree/", views.get_comment_tree),

    #media配置
    re_path(r"media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),

    re_path('^(?P<username>\w+)/articles/(?P<article_id>\d+)$', views.article_detail),

    #关于条件跳转的url
    re_path('^(?P<username>\w+)/(?P<condition>tag|category|archive)/(?P<param>.*)/$', views.home_site),

    #关于个人站点的url
    re_path('^(?P<username>\w+)/$', views.home_site)





]
