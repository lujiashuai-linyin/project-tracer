from django import forms
from django.core.exceptions import ValidationError

from tracer import models
from tracer.form.bootstrap import BootStrapForm


class IssueTypeForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = models.IssuesType
        fields = ['title', ]

    def clean_title(self):
        title = self.cleaned_data['title']
        exist = models.IssuesType.objects.filter(title=title)
        if exist:
            raise ValidationError("问题类型名重复")
        return title

class ModuleForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = models.Module
        fields = ['title', ]

class AppRequireForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = models.AppRequire
        fields = ['title', 'content']

class DeveloperDebugForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = models.DeveloperDebug
        fields = ['title', 'content']
