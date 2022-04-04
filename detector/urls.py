from django.urls import path, re_path, include
from mysite import settings
from detector.views import home

urlpatterns = [
    path('parser/index/', home.index, name='parser_index'),
    path('parser/login/', home.login, name='parser_login'),

]