#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

from tracer import models

class Tracer(object):

    def __init__(self):
        self.user = None
        self.price_policy = None
        self.project = None

class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        """ 如果用户已登录，则request中赋值 """

        request.tracer = Tracer()
        user_id = request.session.get('_auth_user_id', 0)
        user_object = models.UserInfo.objects.filter(nid=user_id).first()
        request.tracer.user = user_object
        # 白名单：没有登录都可以访问的URL
        """
        1. 获取当用户访问的URL
        2. 检查URL是否在白名单中，如果再则可以继续向后访问，如果不在则进行判断是否已登录
        """
        if request.path_info in settings.WHITE_REGEX_URL_LIST:
            return

        # 检查用户是否已登录，已登录继续往后走；未登录则返回登录页面。
        if not request.user.is_authenticated:
            return redirect('login')

        #登录成功后，访问后台管理时，获取当前用户所拥有的额度
        #方式一：免费额度在交易记录中储存
        #获取当前用户id最大的交易记录
        _object = models.Transaction.objects.filter(user=user_object, status=2).order_by('-id').first()
        #判断是否已经过期
        current_datetime = datetime.datetime.now()
        if _object.end_datetime and _object.end_datetime < current_datetime:
            _object = models.Transaction.objects.filter(user=user_object, status=2, price_policy__category=1).first()
        request.price_policy = _object.price_policy