import collections
import datetime
import json
import time

from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from utils.pagination import Pagination
from mysite import settings
from tracer import models
from tracer.models import TikTokAutoTest
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse

from tracer.form.result_filter import ResultFilter


def result_search(request, project_id):
    query_dict = request.GET.copy()
    for name in ['platform', 'version_detail', 'task_id', 'test_path', 'event', 'test_case_url', 'result', 'datetime']:
        value_list = request.GET.getlist(name, None)

        if not value_list[0]:
            query_dict._mutable = True
            query_dict.pop(name)
            continue
        query_dict._mutable = True
        query_dict.pop(name)
        query_dict.setlist(name, value_list)
        # print(value_list)
    if 'page' in query_dict:
        query_dict.pop('page')
    param_url = query_dict.urlencode()
    if param_url:
        base_url = reverse('project_detail', kwargs={'project_id': project_id})
        url = "{}?{}".format(base_url, param_url)
    else:
        url = request.path_info

    return JsonResponse({'status': True, 'url': url})

# 埋点自动化结果

def project_detail(request, project_id):

    kwargs = {'project_id': project_id}

    task_id_list = request.GET.getlist('task_id')
    if len(task_id_list) == 1:
        task_id = list(task_id_list[0].split(','))
    else:
        task_id = task_id_list
    if task_id:
        kwargs.update({'task_id__in': task_id})

    event = request.GET.getlist('event')
    if event:
        kwargs.update({'event__in': event})
    platform = request.GET.getlist('platform')
    if platform:
        kwargs.update({'platform__in': platform})
    version_detail = request.GET.getlist('version_detail')
    if version_detail:
        kwargs.update({'version_detail__in': version_detail})
    test_path = request.GET.getlist('test_path')
    if test_path:
        kwargs.update({'test_path__in': test_path})
    test_case_url = request.GET.getlist('test_case_url')
    if test_case_url:
        kwargs.update({'test_case_url__in': test_case_url})
    result = request.GET.getlist('result')
    if result:
        kwargs.update({'result__in': result})
    create_time = request.GET.getlist('create_time')
    if create_time:
        kwargs.update({'create_time__in': create_time})

    queryset = models.TikTokAutoTest.objects.filter(**kwargs).order_by('-id').all()

    no_version_object = queryset.values('task_id').filter(version_detail__isnull=True).all()

    if no_version_object.exists():
        have_version_object = queryset.values('task_id').distinct().order_by('task_id')
        for item in have_version_object:
            # print(item['task_id'])
            # print(item['version_detail'])
            try:
                version_detail = queryset.filter(task_id=item['task_id'], version_detail__isnull=False).first().version_detail
                no_version_object.filter(task_id=item['task_id']).update(version_detail=version_detail)
            except:
                pass
    queryset_true = models.TikTokAutoTest.objects.filter(**kwargs).order_by('-id').all()
    page_object_true = Pagination(
        current_page=request.GET.get('page'),
        all_count=queryset_true.count(),
        base_url=request.path_info,
        query_params=request.GET
    )
    result_object_list = queryset_true[page_object_true.start:page_object_true.end]
    # for result_object in issues_object_list:
    #     rows.append(
    #         {
    #             'platform': result_object.get_platform_display(),
    #             'version_detail': result_object.version_detail,
    #             'task_id': result_object.task_id,
    #             'test_path': result_object.test_path,
    #             'event': result_object.event,
    #             'test_case_url': result_object.test_case_url,
    #             'result': result_object.result,
    #             'create_time': str(result_object.create_time),
    #         }
    #     )
    form = ResultFilter()

    context = {
        'status': True,
        'form': form,
        'issues_object_list': result_object_list,
        'page_html': page_object_true.page_html(),
    }

    return render(request, 'project_detail.html', context)


# 埋点入库
@csrf_exempt
def result_save(request, project_id):
    """
    { "weekendCaseName": '',
            "platform": "Android",
            "versionDetail": settings.PACKET_VERSION_DETAIL,
            "taskId": int(task_id),
            "caseEvent": label,
            "bitsProjectId": 66666669,
            "bitsCaseId": int(self.case_id),
            "caseResult": False,
        }
    :param request:
    :param project_id:
    :return:

    """
    if request.method == 'POST':
        postBody = request.body
        json_data = json.loads(postBody)
        platform = json_data.get('platform')
        platform_value = None
        # print(platform)
        if platform == 'Android':
            platform_value = 1
        elif platform == 'iOS':
            platform_value = 2
        else:
            return JsonResponse({'status': False, 'error': '平台输入错误'})
        version_detail = json_data.get('versionDetail')
        task_id = json_data.get('taskId')
        test_path = json_data.get('weekendCaseName')
        event = json_data.get('caseEvent')
        bitsCaseId = json_data.get('bitsCaseId')
        bitsProjectId = json_data.get('bitsProjectId')
        test_case_url = (
            settings.CASE_BASE_URL
            + 'projectId='
            + str(bitsProjectId)
            + '&caseId='
            + str(bitsCaseId)
        )
        result = json_data.get('caseResult')
        kwargs = {
            'project_id': project_id,
            'platform': platform_value,
            'version_detail': version_detail,
            'task_id': task_id,
            'test_path': test_path,
            'event': event,
            'test_case_url': test_case_url,
            'case_id': bitsCaseId,
            'result': result,
        }
        exist = models.TikTokAutoTest.objects.filter(task_id=task_id, case_id=bitsCaseId).exists()
        if exist:
            models.TikTokAutoTest.objects.filter(task_id=task_id, case_id=bitsCaseId).update(**kwargs)
            return JsonResponse({'status': True, 'data': '数据库更新成功'})
        try:
            models.TikTokAutoTest.objects.create(**kwargs)
        except:
            return JsonResponse({'status': False, 'error': '数据库存储错误'})
        return JsonResponse({'status': True, 'data': '数据库存储成功'})
    return HttpResponse({'status': True, 'data': '请发送post请求'})


def dashboard(request, project_id):
    # 问题数据处理
    status_dict = collections.OrderedDict()
    for key, text in models.Issues.status_choices:
        status_dict[key] = {'text': text, 'count': 0}

    issues_data = (
        models.Issues.objects.filter(project_id=project_id)
        .values('status')
        .annotate(ct=Count('id'))
    )

    for item in issues_data:
        status_dict[item['status']]['count'] = item['ct']

    # 项目成员
    user_list = models.ProjectUser.objects.filter(project_id=project_id).values(
        'user_id', 'user__username'
    )

    # 最近的10个问题
    top_ten = models.Issues.objects.filter(
        project_id=project_id, assign__isnull=False
    ).order_by('-id')[0:10]

    context = {
        "status_dict": status_dict,
        "user_list": user_list,
        "top_ten_object": top_ten,
    }

    return render(request, 'dashboard.html', context)


def issues_chart(request, project_id):
    """在概览页面生成highcharts所需的数据"""
    today = datetime.datetime.now().date()
    date_dict = collections.OrderedDict()
    for i in range(0, 30):
        date = today - datetime.timedelta(days=i)
        date_dict[date.strftime("%Y-%m-%d")] = [time.mktime(date.timetuple()) * 1000, 0]

    # select xxxx,1 as ctime from xxxx
    # select id,name,email from table;
    # select id,name, strftime("%Y-%m-%d",create_datetime) as ctime from table;
    # "DATE_FORMAT(web_transaction.create_datetime,'%%Y-%%m-%%d')"
    result = (
        models.Issues.objects.filter(
            project_id=project_id,
            create_datetime__gte=today - datetime.timedelta(days=30),
        )
        .extra(
            select={'ctime': "DATE_FORMAT(tracer_issues.create_datetime,'%%Y-%%m-%%d')"}
        )
        .values('ctime')
        .annotate(ct=Count('id'))
    )

    for item in result:
        date_dict[item['ctime']][1] = item['ct']

    return JsonResponse({'status': True, 'data': list(date_dict.values())})
