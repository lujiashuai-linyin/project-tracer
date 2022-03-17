import time

from django.shortcuts import render, redirect

from tracer import models
from tracer.form.project import ProjectModelForm
from django.http import JsonResponse

from utils.tencent.cos import create_bucket
from xpinyin import Pinyin

def project_list(request):
    # print(request.tracer.user.username)
    # print(request.price_policy.project_member)

    if request.method == 'GET':
        # GET请求查看项目列表
        """
        1. 从数据库中获取两部分数据
            我创建的所有项目：已星标、未星标
            我参与的所有项目：已星标、未星标
        2. 提取已星标
            列表 = 循环 [我创建的所有项目] + [我参与的所有项目] 把已星标的数据提取
    
        得到三个列表：星标、创建、参与
        """
        project_dict = {'star': [], 'my': [], 'join': []}

        my_project_list = models.Project.objects.filter(creator=request.user)
        for row in my_project_list:
            if row.star:
                project_dict['star'].append({'value': row, 'type': 'my'})
            else:
                project_dict['my'].append(row)
        join_project_list = models.ProjectUser.objects.filter(user=request.user)
        for item in join_project_list:
            if item.star:
                project_dict['star'].append({'value': item.project, 'type': 'join'})
            else:
                project_dict['join'].append(item.project)

        form = ProjectModelForm(request)
        all_project = models.Project.objects.all()
        return render(request, 'project_list.html', {'form': form, 'project_dict': project_dict, 'all_project': all_project})

    #POST，对话框的ajax添加项目
    response = {'status': None, 'msg': None}
    form = ProjectModelForm(request, data=request.POST)
    if form.is_valid():
        response['status'] = True
        #为项目创建一个桶 & 跨域规则

        bucket = f"tracer-{request.user.pk}-{form.instance.id}-{str(int(time.time()))}-1309571620"
        region = 'ap-beijing'
        create_bucket(bucket, region=region)

        form .instance.bucket = bucket
        form.instance.region = region
        form.instance.creator = request.user
        #创建项目
        form.save()
        return JsonResponse(response)

    else:
        response['status'] = False
        response['msg'] = form.errors
        return JsonResponse(response)

def project_star(request, project_type, project_id):
    if project_type == 'my':
        models.Project.objects.filter(id=project_id, creator=request.user).update(star=True)
        return redirect('project_list')
    if project_type == 'join':
        models.ProjectUser.objects.filter(project_id=project_id, user=request.user).update(star=True)
        return redirect('project_list')
def project_unstar(request, project_type, project_id):
    if project_type == 'my':
        models.Project.objects.filter(id=project_id, creator=request.user).update(star=False)
        return redirect('project_list')
    if project_type == 'join':
        models.ProjectUser.objects.filter(project_id=project_id, user=request.user).update(star=False)
        return redirect('project_list')

def project_application(request, project_id):
    user = request.user
    try:
        exist = models.ProjectUser.objects.filter(project_id=project_id, user=user).exists()
        if exist:
            redirect('project_list')
        else:
            models.ProjectUser.objects.create(project_id=project_id, user=user)
    except:
        pass
    return redirect('project_list')
