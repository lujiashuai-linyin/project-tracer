from django.http import JsonResponse
from django.shortcuts import render, redirect

from tracer import models
from tracer.form.setting import IssueTypeForm, AppRequireForm, DeveloperDebugForm
from utils.tencent.cos import delete_bucket


def setting(request, project_id):
    return render(request, 'setting.html')

def delete(request, project_id):
    if request.method == 'GET':
        return render(request, 'setting_delete.html')

    project_name = request.POST.get('project_name')
    if not project_name or project_name != request.tracer.project.name:
        return render(request, 'setting_delete.html', {'error': "项目名错误"})

    # 项目名写对了则删除（只有创建者可以删除）
    if request.user != request.tracer.project.creator:
        return render(request, 'setting_delete.html', {'error': "只有项目创建者可删除项目"})

    # 1. 删除桶
    #       - 删除桶中的所有文件（找到桶中的所有文件 + 删除文件 )
    #       - 删除桶中的所有碎片（找到桶中的所有碎片 + 删除碎片 )
    #       - 删除桶
    # 2. 删除项目
    #       - 项目删除

    delete_bucket(request.tracer.project.bucket, request.tracer.project.region)
    models.Project.objects.filter(name=project_name, creator=request.user).delete()

    return redirect("project_list")

def add_issuetype(request, project_id):

    if request.method == 'GET':
        return render(request, 'setting_issuetype.html')
    form = IssueTypeForm(data=request.POST)
    if form.is_valid():
        form.instance.project = request.tracer.project
        instance = form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})

def delete_issuetype(request, project_id):
    issuetype_name = request.POST.get('title')
    if not issuetype_name:
        return JsonResponse({'error': "问题类型名称输入错误"})

    if request.user != request.tracer.project.creator:
        return JsonResponse({'error': "只有项目创建者可删除项目"})
    try:
        models.IssuesType.objects.filter(title=issuetype_name, project_id=project_id).delete()
    except:
        return JsonResponse({"status": False, "error": "没有此问题类型"})
    return JsonResponse({"status": True})

def app_require(request, project_id):
    if request.method == 'GET':
        return render(request, 'setting_apprequire.html')
    form = AppRequireForm(data=request.POST)
    if form.is_valid():
        form.instance.project = request.tracer.project
        form.instance.creator = request.user
        form.instance.update_user = request.user
        instance = form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})

def delete_app_require(request, project_id):
    require_title = request.POST.get('title')
    if not require_title:
        return JsonResponse({'error': "需求名称不能为空"})

    if request.user != request.tracer.project.creator:
        return JsonResponse({'error': "只有项目创建者可删除项目"})
    try:
        models.AppRequire.objects.filter(title=require_title, project_id=project_id).delete()
    except:
        return JsonResponse({"status": False, "error": "没有此需求"})
    return JsonResponse({"status": True})

def debug(request, project_id):
    if request.method == 'GET':
        return render(request, 'setting_debug.html')
    form = DeveloperDebugForm(data=request.POST)
    if form.is_valid():
        form.instance.project = request.tracer.project
        form.instance.creator = request.user
        instance = form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})