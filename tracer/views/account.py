import random

import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from django.contrib import auth
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from mysite import settings
from tracer.models import UserInfo
from tracer.my_forms import UserForm
from utils.tencent.sms import send_sms_single

#与用户注册登录相关

def register(request):
    '''
    register view
    '''
    if request.method == 'POST':
        conn = get_redis_connection('default')
        form = UserForm(request.POST)

        response = {'user': None, 'msg': None}
        if form.is_valid():
            telephone = form.cleaned_data.get('telephone')
            code = int(form.cleaned_data.get('code'))
            print(code)
            valid_code = conn.get(telephone)
            valid_code = int(bytes.decode(valid_code))
            print(valid_code)
            if code == valid_code:
                response['user'] = form.cleaned_data.get('user')
                user = form.cleaned_data.get("user")
                print(user)
                pwd = form.cleaned_data.get('pwd')
                email = form.cleaned_data.get('email')
                telephone = form.cleaned_data.get('telephone')
                avatar_obj = request.FILES.get('avatar')
                extra = {}
                if avatar_obj:
                    extra['avatar'] = avatar_obj

                user_obj = UserInfo.objects.create_user(username=user, password=pwd, email=email, telephone=telephone, **extra)
            else:
                response['msg'] = '请输入正确的验证码'
        else:
            print(form.cleaned_data)
            print(form.errors)
            response['msg'] = form.errors

        return JsonResponse(response)
    form = UserForm()

    return render(request, 'register.html', {'form': form})


from django.shortcuts import HttpResponse
from django_redis import get_redis_connection
def register_valid_code(request):
    response = {"user":None,"result":None}
    conn = get_redis_connection('default')
    telephone = request.POST.get('telephone')
    #自己开发时未做二次校验

    template_id = settings.TENCENT_SMS_TEMPLATE['register']
    template_param_list = random.randrange(1000, 9999)
    conn.set(telephone, template_param_list, ex=30)
    print(template_param_list)
    # response = send_sms_single(telephone, template_id, template_param_list=[template_param_list, ])

    return JsonResponse(response)



def get_validCode_img(request):
    '''
    基于PIL模块生成响应状态图片
    '''
    from utils.tracer.valid_code import get_validCode_img
    img_data = get_validCode_img(request)
    return HttpResponse(img_data)

def login(request):
    if request.method == 'POST':

        response = {'user': None, 'msg': None}
        user = request.POST.get("user")
        pwd = request.POST.get('pwd')
        valid_code = request.POST.get('valid_code')

        valid_code_str = request.session.get('valid_code_str')
        if valid_code.upper() == valid_code_str.upper():
            user = auth.authenticate(username=user, password=pwd)
            if user:
                auth.login(request, user)
                response['user'] = user.username
            else:
                response['msg'] = '用户名或密码错误'
        else:
            response['msg'] = '验证码错误'

        return JsonResponse(response)

    return render(request, 'login.html')



