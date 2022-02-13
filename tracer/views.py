from django.contrib import auth
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from tracer.models import UserInfo
from tracer.my_forms import UserForm

def register(request):
    '''
    register view
    '''
    if request.method == 'POST':
        print(request.POST)
        form = UserForm(request.POST)

        response = {'user': None, 'msg': None}
        if form.is_valid():
            print(form.cleaned_data)
            response['user'] = form.cleaned_data.get('user')
            user = form.cleaned_data.get("user")
            pwd = form.cleaned_data.get('pwd')
            email = form.cleaned_data.get('email')
            telephone = form.cleaned_data.get('telephone')
            avatar_obj = request.FILES.get('avatar')

            extra = {}
            if avatar_obj:
                extra['avatar'] = avatar_obj
                user_obj = UserInfo.objects.create_user(username=user, password=pwd, email=email, telephone=telephone, **extra)

        else:
            print(form.cleaned_data)
            print(form.errors)
            response['msg'] = form.errors

        return JsonResponse(response)
    form = UserForm()

    return render(request, 'register.html', {'form': form})

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