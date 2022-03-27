from django import forms

from tracer import models
from tracer.form.bootstrap import BootStrapForm


class IssuesModelForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = models.Issues
        fields = ['subject', 'creator', 'module', 'issues_type', 'desc', 'require', 'status', 'priority', 'assign', 'attention', 'start_date', 'end_date', 'mode', 'parent']
        widgets = {
            "assign": forms.Select(attrs={"title": "请选择", 'class': "selectpicker", "data-live-search": "true", "data-dropup-auto": "false"}),
            "module": forms.SelectMultiple(attrs={"title": "请选择", 'class': "selectpicker", "data-live-search": "true"}),
            "require": forms.SelectMultiple(attrs={"title": "请选择", 'class': "selectpicker", "data-live-search": "true"}),
            "attention": forms.SelectMultiple(attrs={"title": "请选择", 'class': "selectpicker", "data-live-search": "true", "data-actions-box": "true"}),
            "parent": forms.Select(attrs={"title": "请选择", 'class': "selectpicker", "data-live-search": "true"}),
            "start_date": forms.DateTimeInput(attrs={"title": "请选择", 'autocomplete': "off"}),
            "end_date": forms.DateTimeInput(attrs={"title": "请选择", 'autocomplete': "off"}),
            "issues_type": forms.Select(attrs={"title": "请选择", 'class': "selectpicker", "data-live-search": "true"})
            }

    def __init__(self, request, *args, **kwargs):
        super(IssuesModelForm, self).__init__(*args, **kwargs)
        # 处理数据初始化
        #补充
        self.fields['require'].choices = models.AppRequire.objects.filter(project=request.tracer.project).values_list('id', 'title')
        # 1.获取当前项目的所有问题类型 [(1,'xx'),(2,"xx")]
        self.fields['issues_type'].choices = models.IssuesType.objects.filter(project=request.tracer.project).values_list('id', 'title')

        #模块
        module_list = []
        module_object_list = models.Module.objects.filter(project=request.tracer.project).values_list('id', 'title')
        module_list.extend(module_object_list)
        self.fields['module'].choices = module_list
        #
        # # 3.指派和关注者
        # # 数据库找到当前项目的参与者 和 创建者
        total_user_list = [(request.tracer.project.creator_id, request.tracer.project.creator.username), ]
        project_user_list = models.ProjectUser.objects.filter(project=request.tracer.project).values_list('user_id',
                                                                                                          'user__username')
        total_user_list.extend(project_user_list)

        self.fields['assign'].choices = total_user_list
        self.fields['attention'].choices = total_user_list

        # #4. 当前项目已创建的问题
        parent_list = []
        parent_object_list = models.Issues.objects.filter(project=request.tracer.project).values_list('id', 'subject')
        parent_list.extend(parent_object_list)
        self.fields['parent'].choices = parent_list

class IssuesReplyModelForm(forms.ModelForm):
    class Meta:
        model = models.IssuesReply
        fields = ['content', 'reply']

class InviteModelForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = models.ProjectInvite
        fields = ['period', 'count']