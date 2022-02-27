from django.shortcuts import render, redirect
from django.urls import reverse

from tracer import models
from tracer.form.project import ProjectModelForm
from django.http import JsonResponse

from tracer.form.wiki import WikiModelForm


def wiki(request, project_id):
    if request.method == 'GET':
        form = WikiModelForm(request)
        return render(request, 'wiki.html', {'form': form})


def wiki_add(request, project_id):
    if request.method == 'GET':
        form = WikiModelForm(request)
        return render(request, 'wiki_add.html', {'form': form})

    form = WikiModelForm(request, data=request.POST)
    if form.is_valid():
        form.instance.user = request.user
        form.instance.project = request.tracer.project
        form.save()
        url = reverse('wiki', kwargs={'project_id': project_id})
        return redirect(url)
    return render(request, 'wiki_add.html', {'form': form})


def wiki_catalog(request, project_id):
    data = models.Wiki.objects.filter(project=project_id, parent='').values('id', 'title')
    return JsonResponse({'status': True, 'data': list(data)})

def wiki_delete(request):
    pass

def wiki_edit(request):
    pass

def wiki_upload(request):
    pass
