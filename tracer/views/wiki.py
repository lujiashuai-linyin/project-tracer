from django.shortcuts import render, redirect

from tracer import models
from tracer.form.project import ProjectModelForm
from django.http import JsonResponse

from tracer.form.wiki import WikiModelForm


def wiki(request, project_id):
    form = WikiModelForm(request)
    return render(request, 'wiki.html', {'form': form})

def wiki_add(request):
    pass

def wiki_catalog(request):
    pass

def wiki_delete(request):
    pass

def wiki_edit(request):
    pass

def wiki_upload(request):
    pass
