import collections
import datetime
import json
import time

from django.db.models import Count

from tracer import models
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse

from tracer.form.result_filter import ResultFilter


def project_detail(request, project_id):
    form = ResultFilter()
    return render(request, 'project_detail.html', {'form': form})

def dashboard(request, project_id):
    # 问题数据处理
    status_dict = collections.OrderedDict()
    for key, text in models.Issues.status_choices:
        status_dict[key] = {'text': text, 'count': 0}

    issues_data = models.Issues.objects.filter(project_id=project_id).values('status').annotate(ct=Count('id'))
    for item in issues_data:
        status_dict[item['status']]['count'] = item['ct']

    # 项目成员
    user_list = models.ProjectUser.objects.filter(project_id=project_id).values('user_id', 'user__username')

    # 最近的10个问题
    top_ten = models.Issues.objects.filter(project_id=project_id, assign__isnull=False).order_by('-id')[0:10]

    context = {
        "status_dict": status_dict,
        "user_list": user_list,
        "top_ten_object": top_ten
    }

    return render(request, 'dashboard.html', context)


def test_result(request, project_id):
    #获取request请求中的筛选参数,自创搜索引擎，还算牛掰
    kwargs = {'project_id': project_id}

    task_id = request.GET.get('task_id')

    if task_id:

        kwargs.update({'task_id': task_id})

    event = request.GET.get('event')
    if event:
        kwargs.update({'event': event})
    platform = request.GET.get('platform')
    if platform:

        kwargs.update({'platform': platform})
    version_detail = request.GET.get('version_detail')
    if version_detail:
        kwargs.update({'version_detail': version_detail})
    test_path = request.GET.get('test_path')
    if test_path:
        kwargs.update({'test_path': test_path})
    test_case_url = request.GET.get('test_case_url')
    if test_case_url:
        kwargs.update({'test_case_url': test_case_url})
    result = request.GET.get('result')
    if result:
        kwargs.update({'result': result})
    create_time = request.GET.get('create_time')
    if create_time:
        kwargs.update({'create_time': create_time})

    rows = []


    result_list = models.TikTokAutoTest.objects.filter(**kwargs).all()

    for result_object in result_list:
        rows.append(
            {
                'platform': result_object.get_platform_display(),
                'version_detail': result_object.version_detail,
                'task_id': result_object.task_id,
                'test_path': result_object.test_path,
                'event': result_object.event,
                'test_case_url': result_object.test_case_url,
                'result': result_object.result,
                'create_time': str(result_object.create_time)
            }
        )
    total = len(rows)
    data = {"status": 0, "extra_msg": None, "total": total, "rows": rows}

    return HttpResponse(json.dumps(data))

def issues_chart(request, project_id):
    """ 在概览页面生成highcharts所需的数据 """
    today = datetime.datetime.now().date()
    date_dict = collections.OrderedDict()
    for i in range(0, 30):
        date = today - datetime.timedelta(days=i)
        date_dict[date.strftime("%Y-%m-%d")] = [time.mktime(date.timetuple()) * 1000, 0]

    # select xxxx,1 as ctime from xxxx
    # select id,name,email from table;
    # select id,name, strftime("%Y-%m-%d",create_datetime) as ctime from table;
    # "DATE_FORMAT(web_transaction.create_datetime,'%%Y-%%m-%%d')"
    result = models.Issues.objects.filter(project_id=project_id,
                                          create_datetime__gte=today - datetime.timedelta(days=30)).extra(
        select={'ctime': "DATE_FORMAT(tracer_issues.create_datetime,'%%Y-%%m-%%d')"}).values('ctime').annotate(ct=Count('id'))

    for item in result:
        date_dict[item['ctime']][1] = item['ct']

    return JsonResponse({'status': True, 'data': list(date_dict.values())})