from django import forms
from django.core.exceptions import ValidationError

from tracer import models
from tracer.form.widgets import ColorRadioSelect
from tracer.form.bootstrap import BootStrapForm

class ProjectModelForm(BootStrapForm, forms.ModelForm):
    bootstrap_class_exclude = ['color']
    # desc = forms.CharField(widget=forms.Textarea())
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
    class Meta:
        model = models.Project
        fields = ['name', 'color', 'desc']
        widgets = {
            'desc': forms.Textarea,
            'color': ColorRadioSelect(attrs={'class': 'color-radio'})
        }
        error_messages={
            'name': {'required': '项目名不能为空'}
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        #1. 当前用户是否已经创建此项目
        exists = models.Project.objects.filter(name=name, creator=self.request.user).exists()
        if exists:
            raise ValidationError('项目名已存在')
        #2. 当前用户是否还有额度进行项目创建？
        user_project_num = models.Project.objects.filter(creator=self.request.user).count()
        project_num = self.request.tracer.price_policy.project_num
        if user_project_num >= project_num:
            raise ValidationError('项目个数已超限，请购买套餐')
        return name
