from rest_framework.routers import DefaultRouter
from django.urls import path, re_path, include
from mysite import settings
from detector.views import home
from detector.views import student

router = DefaultRouter()
router.register("student", student.StudentmodelsViewSet, basename="student")
urlpatterns = [
    # path('index/', home.index, name='parser_index'),
    # path('login/', home.login, name='parser_login'),
    path('ser/', student.StudentView.as_view())

] + router.urls