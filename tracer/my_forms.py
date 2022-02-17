from django import forms
from django.forms import widgets
from tracer import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class UserForm(forms.Form):
    user = forms.CharField(max_length=32,
                           label='用户名',)
    pwd = forms.CharField(max_length=32,
                          label='密码',
                          widget=forms.PasswordInput())
    re_pwd = forms.CharField(max_length=32,
                             label='确认密码',
                             widget=forms.PasswordInput())
    email = forms.EmailField(max_length=32,
                             label='电子邮箱',)
    telephone = forms.CharField(
        label='手机号',
        validators=[
            RegexValidator(
                r'^1(3|4|5|6|7|8|9)\d{9}$',
                '手机号格式错误'),
        ],
    )
    code = forms.CharField(
        label="验证码")

    class Mate:
        model = models.UserInfo
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs["class"] = 'form-control'
            field.widget.attrs["placeholder"] = "请输入%s" % (field.label, )
