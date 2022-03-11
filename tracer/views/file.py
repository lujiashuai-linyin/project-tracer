from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from tracer import models


def file(request, project_id):
    url_list = []
    file_id = request.GET.get('file_id')
    if not file_id:
        url = reverse('file', kwargs={'project_id': project_id})
        return redirect(url)

    file_object = models.FileRepository.objects.filter(id=file_id, project_id=project_id, file_type=2).first()
    while file_object:
        url_list.insert(0, file_object.name)
        file_object = file_object.parent
    return JsonResponse({''})

def file_delete(request):
    pass
def cos_credential(request):
    pass
def file_post(request):
    pass
def file_download(request):
    pass
