import json

from tracer import models
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse


def project_detail(request, project_id):
    return render(request, 'project_detail.html')


def issues_chart(request):
    pass


def test_result(request, project_id):
    task_id = request.GET.get('task_id')
    result_list = models.TikTokAutoTest.objects.all()
    rows = []
    for result_object in result_list:
        rows.append(
            {
                'platform': result_object.platform,
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
