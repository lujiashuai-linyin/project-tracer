import datetime
import random

import ssl
import uuid

from django.db.models import Q

from tracer import models

ssl._create_default_https_context = ssl._create_unverified_context
from django.contrib import auth
from django.http import JsonResponse
from django.shortcuts import render, redirect

from mysite import settings
from tracer.models import UserInfo
from tracer.form.account import UserForm, SendSmsForm, LoginSMSForm, LoginForm
from utils.tencent.sms import send_sms_single

#与用户注册登录相关

def register(request):
    '''
    register view
    '''
    if request.method == 'POST':

        form = UserForm(request.POST)

        response = {'user': None, 'msg': None}
        if form.is_valid():
            user = form.data.get('user')
            response['user'] = user
            pwd = form.data.get('pwd')
            email = form.data.get('email')
            telephone = form.data.get('telephone')
            avatar_obj = request.FILES.get('avatar')
            extra = {}
            if avatar_obj:
                extra['avatar'] = avatar_obj
            UserInfo.objects.create_user(username=user, password=pwd, email=email, telephone=telephone, **extra)
        #写入数据库nb方法,但是密码明文保存
            # form.save()
            #方法一
            # price_policy = models.PricePolicy.objects.filter(category=1, title='个人免费版').first()
            # models.Transaction.objects.create(
            #     status=2,
            #     order=str(uuid.uuid4()),
            #     user=user_obj,
            #     price_policy=price_policy,
            #     count=0,
            #     price=0,
            #     start_datetime=datetime.datetime.now(),
            # )
            #方法二
        else:
            response['msg'] = form.errors

        return JsonResponse(response)
    form = UserForm()

    return render(request, 'register.html', {'form': form})


from django.shortcuts import HttpResponse
from django_redis import get_redis_connection
def register_valid_code(request):
    response = {"result": None, "msg": None}
    #自己开发时未做二次校验
    form = SendSmsForm(request, data=request.GET)
    if form.is_valid():
        response['result'] = True
    else:
        response['result'] = False
        response['msg'] = form.errors
    return JsonResponse(response)

def get_validCode_img(request):
    '''
    基于PIL模块生成响应状态图片
    '''
    from utils.tracer.valid_code import get_validCode_img
    img_data = get_validCode_img(request)
    return HttpResponse(img_data)

def login_sms(request):
    """ 短信登录 """
    response = {"user": None, "msg": None}
    if request.method == 'GET':
        form = LoginSMSForm()
        return render(request, 'login_sms.html', {'form': form})
    form = LoginSMSForm(request.POST)
    if form.is_valid():
        # 用户输入正确，登录成功
        mobile_phone = form.cleaned_data['telephone']
        user = models.UserInfo.objects.filter(telephone=mobile_phone).first()
        # 把用户名写入到session中#重点！
        auth.login(request, user)
        response['user'] = user.username

        return JsonResponse(response)
    else:
        response['msg'] = form.errors

    return JsonResponse(response)

def login(request):
    if request.method == 'POST':

        response = {'user': None, 'msg': None}
        username = request.POST.get("username")
        password = request.POST.get('password')
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user_object = models.UserInfo.objects.filter(Q(email=username) | Q(telephone=username)).first()
            user = auth.authenticate(username=user_object.username, password=password)
            if user:
                auth.login(request, user)
                response['user'] = user.username
            else:
                response['msg'] = {'username': ['用户名或密码错误', ]}
        else:
            response['msg'] = form.errors

        return JsonResponse(response)

    form = LoginForm(request)

    return render(request, 'login.html', {'form': form})

def index(request):
    return render(request, 'index.html')

def logout(request):

    # auth.logout(request)
    request.session.flush()

    return redirect('/index/')
