#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import forms

from tracer import models
from tracer.form.bootstrap import BootStrapForm


class WikiModelForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = models.Wiki
        exclude = ['project', 'depth', 'create_time', 'user']
        error_messages = {
            'title': {'required': '标题不能为空'},
            'content': {'request': '内容不能为空'}
        }

        def __init__(self, request, *args, **kwargs):
            super().__init__(*args, **kwargs)