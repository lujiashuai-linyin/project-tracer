import json

from tracer import models
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse

from tracer.form.result_filter import ResultFilter


def project_detail(request, project_id):
    form = ResultFilter()
    return render(request, 'project_detail.html', {'form': form})


def issues_chart(request):
    pass


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

