from django.template import Library
from django.urls import reverse

from tracer import models

register = Library()

@register.inclusion_tag('inclusion/all_project_list.html')
def all_project_list(request):
    # 1. 获我创建的所有项目
    my_project_list = models.Project.objects.filter(creator=request.user)

    # 2. 获我参与的所有项目
    join_project_list = models.ProjectUser.objects.filter(user=request.user)

    return {'my': my_project_list, 'join': join_project_list, 'request': request}

@register.inclusion_tag('inclusion/manage_menu_list.html')
def manage_menu_list(request):
    data_list = [
        {'title': '埋点', 'url': reverse("project_detail", kwargs={'project_id': request.tracer.project.id})},
        {'title': '场景', 'url': reverse("mock_scene", kwargs={'project_id': request.tracer.project.id})},
        {'title': '概览', 'url': reverse("dashboard", kwargs={'project_id': request.tracer.project.id})},
        {'title': '问题', 'url': reverse("issues", kwargs={'project_id': request.tracer.project.id})},
        {'title': '统计', 'url': reverse("statistics", kwargs={'project_id': request.tracer.project.id})},
        {'title': 'wiki', 'url': reverse("wiki", kwargs={'project_id': request.tracer.project.id})},
        {'title': '文件', 'url': reverse("file", kwargs={'project_id': request.tracer.project.id})},
        {'title': '配置', 'url': reverse("setting", kwargs={'project_id': request.tracer.project.id})},
    ]

    for item in data_list:
        # 当前用户访问的URL：request.path_info:  /manage/4/issues/xxx/add/
        if request.path_info.startswith(item['url']):
            item['class'] = 'active'

    return {'data_list': data_list}