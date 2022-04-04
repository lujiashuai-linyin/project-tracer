from django.shortcuts import render

# Create your views here.
from django.contrib import auth
from django.http import JsonResponse
def index(request):
    return render(request, 'detector/index.html')
def login(request):
    return render(request, 'detector/login.html')