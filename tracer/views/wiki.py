import datetime
import os

from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.csrf import csrf_exempt

from tracer import models
from tracer.form.project import ProjectModelForm
from django.http import JsonResponse, HttpResponse

from tracer.form.wiki import WikiModelForm
from utils.tencent.cos import upload_file
from utils.tracer.encrypt import uid


def wiki(request, project_id):
    wiki_id = request.GET.get('wiki_id')
    #十进制小数
    if not wiki_id or not wiki_id.isdecimal():
        return render(request, 'wiki.html')

    try:
        wiki_object = models.Wiki.objects.filter(id=wiki_id, project_id=project_id).first()
    except:
        return HttpResponse('该项目没有此文章')
    else:
        return render(request, 'wiki.html', {'wiki_object': wiki_object})

def wiki_catalog(request, project_id):
    data = models.Wiki.objects.filter(project=project_id).values('id', 'title', 'parent_id').order_by('depth', 'id')
    return JsonResponse({'status': True, 'data': list(data)})

# def wiki_sub_catalog(request, project_id, wiki_id):
#     data = not models.Wiki.objects.filter(parent_id=wiki_id).values('id', 'title')
#     return JsonResponse({'status': True, 'data': data})

def wiki_add(request, project_id):
    if request.method == 'GET':
        form = WikiModelForm(request)
        return render(request, 'wiki_add.html', {'form': form})

    form = WikiModelForm(request, data=request.POST)
    if form.is_valid():
        if form.instance.parent:
            form.instance.depth = form.instance.parent.depth + 1
        else:
            form.instance.depth = 1
        form.instance.user = request.user
        form.instance.project = request.tracer.project
        form.instance.last_edit_user = request.user
        form.instance.last_edit_time = datetime.datetime.now()
        form.save()
        #此处创建文章与参与人员关系数据，后加入人员将在加入项目反向创建(有更优解)
        models.WikiJoin.objects.create(wiki_id=form.instance.id, user=request.user, editor=True)
        # user_list = models.ProjectUser.objects.filter(project_id=project_id).values_list('user')
        # for user in user_list:
        #     models.WikiJoin.objects.create(wiki_id=form.instance.id, user=user)
        base_url = reverse('wiki', kwargs={'project_id': project_id})
        url = base_url + "?wiki_id=" + str(form.instance.id)
        return redirect(url)
    return render(request, 'wiki_add.html', {'form': form})


def wiki_delete(request, project_id, wiki_id):
    if not wiki_id or not wiki_id.isdecimal():
        return render(request, 'wiki.html')
    wiki_object = models.Wiki.objects.filter(project_id=project_id, id=wiki_id).first()
    #判断文章是否存在
    if not wiki_object:
        # url = reverse('wiki', kwargs={'project_id': project_id})
        return HttpResponse('此项目无此文章')
    try:
        is_editor = models.WikiJoin.objects.filter(wiki_id=wiki_id, user=request.user).first().editor
        if not is_editor:
            return HttpResponse('您无权删除此文章')
    except:
        return HttpResponse('您无权删除此文章')
    models.Wiki.objects.filter(id=wiki_id, project_id=project_id, user=request.user).first().delete()
    url = reverse('wiki', kwargs={'project_id': project_id})
    return redirect(url)

def wiki_edit(request, project_id, wiki_id):
    if not wiki_id or not wiki_id.isdecimal():
        return render(request, 'wiki.html')
    wiki_object = models.Wiki.objects.filter(project_id=project_id, id=wiki_id).first()
    #判断文章是否存在
    if not wiki_object:
        # url = reverse('wiki', kwargs={'project_id': project_id})
        return HttpResponse('此项目无此文章')
    try:
        is_editor = models.WikiJoin.objects.filter(wiki_id=wiki_id, user=request.user).first().editor
        if not is_editor:
            return HttpResponse('您无权编辑此文章')
    except:
        return HttpResponse('您无权编辑此文章')

    if request.method == 'GET':
        form = WikiModelForm(request, instance=wiki_object)
        return render(request, 'wiki_add.html', {'form': form})

    form = WikiModelForm(request, data=request.POST, instance=wiki_object)
    if form.is_valid():
        if form.instance.parent:
            form.instance.depth = form.instance.parent.depth + 1
        else:
            form.instance.depth = 1
        form.instance.last_edit_time = datetime.datetime.now()
        form.instance.last_edit_user = request.user
        form.save()
        # models.Wiki.objects.filter(id=wiki_id, project_id=project_id).update(last_edit_user=request.user, last_edit_time=last_edit_time, depth=depth)
        base_url = reverse('wiki', kwargs={'project_id': project_id})
        url = base_url + "?wiki_id=" + wiki_id
        # print(url)
        return redirect(url)
    # return render(request, 'wiki_add.html', {'form': form})

def wiki_enable(request, project_id, wiki_id):
    '''
    申请人给有编辑权限者发送编辑请求，数据库创建wiki——user关系数据
    :param request:
    :param project_id:
    :param wiki_id:
    :return:
    '''
    exist = models.WikiJoin.objects.filter(user=request.user, wiki_id=wiki_id).exists()
    if not exist:
        models.WikiJoin.objects.create(user=request.user, wiki_id=wiki_id, editor=False)

    #通知有编辑权限的人

def wiki_collection(request, project_id, wiki_id):
    '''
    收藏文章
    :param request:
    :param project_id:
    :param wiki_id:
    :return:
    '''
    exist = models.WikiJoin.objects.filter(user=request.user, wiki_id=wiki_id).exists()
    if not exist:
        models.WikiJoin.objects.create(user=request.user, wiki_id=wiki_id)
    models.WikiJoin.objects.filter(user=request.user, wiki_id=wiki_id).update(collection=True)

def wiki_uncollection(request, project_id, wiki_id):
    '''
    取消收藏
    :param request:
    :param project_id:
    :param wiki_id:
    :return:
    '''
    try:
        models.WikiJoin.objects.filter(user=request.user, wiki_id=wiki_id).update(collection=False)
    except:
        return HttpResponse("您尚未收藏此文章")

@xframe_options_sameorigin
@csrf_exempt
def wiki_upload(request, project_id):
    '''markdown插件图片上传'''
    result = {
        'success': 0,
        'message': None,
        'url': None
    }

    img = request.FILES.get("editormd-image-file")
    if not img:
        result['message'] = "文件不存在"
        return JsonResponse(result)

    ext = img.name.rsplit('.')[-1]
    key = "{}.{}".format(uid(str(request.user.pk)), ext)
    #方式一，保存在本地media
    # path = os.path.join(settings.MEDIA_ROOT, 'add_wiki_img', img.name)
    # with open(path, 'wb') as f:
    #     for line in img:
    #         f.write(line)
    #
    # response = {"status": 0, "url": "/media/add_wiki_img/%s" % img.name}
    # print('ok')
    #方式二，上传通讯云存储
    bucket = request.tracer.project.bucket
    region = request.tracer.project.region
    image_url = upload_file(bucket=bucket, file_path=img, key=key, region=region)
    result['success'] = 1
    result['url'] = image_url

    return JsonResponse(result)
