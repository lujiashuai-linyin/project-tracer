#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import forms

from tracer import models
from tracer.form.bootstrap import BootStrapForm


class WikiModelForm(BootStrapForm, forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)

        total_data_list = [("", "请选择"),]
        data_list = models.Wiki.objects.filter(project=request.tracer.project).values_list('id', 'title')
        total_data_list.extend(data_list)
        self.fields['parent'].choices = total_data_list

    class Meta:
        model = models.Wiki
        exclude = ['project', 'depth', 'create_time', 'user']
        error_messages = {
            'title': {'required': '标题不能为空'},
            'content': {'required': '内容不能为空'}
        }

