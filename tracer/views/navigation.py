from django.shortcuts import render, redirect

from tracer import models


def list_jump(request):
    return render(request, 'extra_page.html')
