from django import forms
from django.forms import widgets
from tracer.models import UserInfo
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class UserForm(forms.Form):
    user = forms.CharField(max_length=32,
                           label='用户名',
                           widget=widgets.TextInput(attrs={"class": "form-control"},))
    pwd = forms.CharField(max_length=32,
                          label='密码',
                          widget=widgets.PasswordInput(attrs={'class': 'form-control'}))
    re_pwd = forms.CharField(max_length=32,
                             label='确认密码',
                             widget=widgets.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=32,
                             label='电子邮箱',
                             widget=widgets.EmailInput(attrs={'class': 'form-control'}))
    telephone = forms.CharField(label='手机号',
                                validators=[RegexValidator(r'^1(3|4|5|6|7|8|9)\d{9}$', '手机号格式错误'), ],
                                widget=widgets.EmailInput(attrs={'class': 'form-control'}))
