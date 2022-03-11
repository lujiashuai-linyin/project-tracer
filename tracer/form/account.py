import random

import requests
from django import forms
from django.forms import widgets
from django_redis import get_redis_connection

from mysite import settings
from tracer import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from tracer.form.bootstrap import BootStrapForm
from utils.tencent.sms import send_sms_single


class UserForm(BootStrapForm, forms.Form):
    user = forms.CharField(
        error_messages={"required": "用户名不能为空"},
        max_length=32,
        label='用户名',
    )
    pwd = forms.CharField(
        label='用户密码',
        min_length=8,
        max_length=64,
        error_messages={'required': '请输入用户密码', 'min_length': "密码长度不能小于8个字符", 'max_length': "密码长度不能大于64个字符"},
        widget=forms.PasswordInput(),
    )
    re_pwd = forms.CharField(
        required=False,
        min_length=8,
        max_length=64,
        error_messages={
            'min_length': "重复密码长度不能小于8个字符",
            'max_length': "重复密码长度不能大于64个字符",
        },
        label='确认密码',
        widget=forms.PasswordInput(),
    )
    email = forms.EmailField(
        required=False,
        error_messages={"required": "邮箱不能为空"},
        max_length=32,
        label='电子邮箱',
    )
    telephone = forms.CharField(
        label='手机号',
        error_messages={"required": "手机号不能为空"},
        validators=[
            RegexValidator(r'^1(3|4|5|6|7|8|9)\d{9}$', message='手机号格式错误'),
        ],
    )
    code = forms.CharField(label="验证码", required=False, widget=forms.TextInput())

    class Mate:
        model = models.UserInfo
        # fields = "__all__"

    def clean_user(self):
        val = self.cleaned_data['user']
        user = models.UserInfo.objects.filter(username=val).exists()
        if not user:
            return val
        else:
            raise ValidationError("该用户已注册")

    def clean(self):
        pwd = self.cleaned_data["pwd"]
        re_pwd = self.cleaned_data["re_pwd"]
        user = self.cleaned_data['user']
        if user and pwd and re_pwd:
            if pwd == re_pwd:
                return re_pwd
            else:
                raise ValidationError("两次密码输入不一致")
        else:
            return self.cleaned_data

    # def clean_password(self):
    #     pwd = self.cleaned_data['password']
    #     # 加密 & 返回
    #     return encrypt.md5(pwd)

    def clean_email(self):
        email = self.cleaned_data['email']
        exists = models.UserInfo.objects.filter(email=email).exists()
        if exists:
            raise ValidationError('邮箱已存在')
        return email

    def clean_telephone(self):
        mobile_phone = self.cleaned_data['telephone']
        exists = models.UserInfo.objects.filter(telephone=mobile_phone).exists()
        if exists:
            raise ValidationError('手机号已注册')
        return mobile_phone

    def clean_code(self):
        code = self.cleaned_data['code']
        mobile_phone = self.cleaned_data['telephone']
        if not mobile_phone:
            return code

        conn = get_redis_connection()
        redis_code = conn.get(mobile_phone)
        if not redis_code:
            raise ValidationError('验证码失效或未发送')

        redis_str_code = redis_code.decode('utf-8')

        if code.strip() != redis_str_code:
            raise ValidationError('验证码错误，请重新输入')

        return code


class SendSmsForm(forms.Form):
    telephone = forms.CharField(
        label="手机号",
        error_messages={"required": "手机号不能为空"},
        validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误')]
    )

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_telephone(self):
        telephone = self.cleaned_data['telephone']
        template = self.request.GET.get('template')
        if template == 'register':
            exist = models.UserInfo.objects.filter(telephone=telephone).exists()
            if exist:
                raise ValidationError('手机号已存在')
        elif template == 'login':
            exist = models.UserInfo.objects.filter(telephone=telephone).exists()
            if not exist:
                raise ValidationError('该手机号未注册')
        template_id = settings.TENCENT_SMS_TEMPLATE.get(template)
        if not template_id:
            # self.add_error('mobile_phone','短信模板错误')
            raise ValidationError('短信模板错误')
        template_param_list = random.randrange(1000, 9999)
        # response = send_sms_single(telephone, template_id, template_param_list=[template_param_list, ])
        print(template_param_list)
        # if response['result'] != 0:
        #     raise ValidationError('短信发送失败，{}'.format(response['errmsg']))

        conn = get_redis_connection('default')
        conn.set(telephone, template_param_list, ex=30)

        return template_param_list

class LoginSMSForm(BootStrapForm, forms.Form):
    telephone = forms.CharField(
        label='手机号',
        error_messages={"required": "手机号不能为空"},
        validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ]
    )

    code = forms.CharField(
        label='验证码',
        error_messages={"required": "请输入验证码"},
        widget=forms.TextInput())

    def clean_telephone(self):
        mobile_phone = self.cleaned_data['telephone']
        exists = models.UserInfo.objects.filter(telephone=mobile_phone).exists()
        # user_object = models.UserInfo.objects.filter(mobile_phone=mobile_phone).first()
        if not exists:
            raise ValidationError('该手机号未注册')

        return mobile_phone
    def clean_code(self):
        code = self.cleaned_data['code']
        mobile_phone = self.cleaned_data['telephone']

        # 手机号不存在，则验证码无需再校验
        if not mobile_phone:
            return code

        conn = get_redis_connection()
        redis_code = conn.get(mobile_phone)  # 根据手机号去获取验证码
        if not redis_code:
            raise ValidationError('验证码失效或未发送')

        redis_str_code = redis_code.decode('utf-8')

        if code.strip() != redis_str_code:
            raise ValidationError('验证码错误，请重新输入')

        return code

class LoginForm(BootStrapForm, forms.Form):
    username = forms.CharField(label='邮箱或手机号', error_messages={"required": "请输入邮箱或手机号"},)
    password = forms.CharField(label='密码', error_messages={"required": "请输入密码"}, widget=forms.PasswordInput(render_value=True))
    valid_code = forms.CharField(label='验证码')

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    # def clean_password(self):
    #     pwd = self.cleaned_data['password']
    #     # 加密 & 返回
    #     return encrypt.md5(pwd)

    def clean_valid_code(self):
        """ 钩子 图片验证码是否正确？ """
        # 读取用户输入的yanzhengma
        code = self.cleaned_data['valid_code']

        # 去session获取自己的验证码
        session_code = self.request.session.get('valid_code_str')
        if not session_code:
            raise ValidationError('验证码已过期，请重新获取')

        if code.strip().upper() != session_code.strip().upper():
            print(session_code)
            raise ValidationError('验证码输入错误')

        return code
