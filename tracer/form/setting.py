from django import forms

from tracer import models
from tracer.form.bootstrap import BootStrapForm


class IssueTypeForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = models.IssuesType
        fields = ['title', ]

class ModuleForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = models.Module
        fields = ['title', ]

class AppRequireForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = models.AppRequire
        fields = ['title', 'content']
