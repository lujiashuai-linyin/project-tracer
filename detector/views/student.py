from rest_framework.viewsets import ModelViewSet
from django.http import JsonResponse
from django.views import View
from detector import models
from detector.serializers.serializers import (
    StudentModelSerializers,
    Student1Serializers,
)


class StudentmodelsViewSet(ModelViewSet):
    queryset = models.Student.objects.all()
    serializer_class = StudentModelSerializers


class StudentView(View):

    def get(self, request):
        # 1.获取模型数据
        student_list = models.Student.objects.all()
        # 2.实例化序列化对象
        serializers = Student1Serializers(instance=student_list, many=True)
        # 3.调用序列化对象的data
        data = serializers.data
        # 4.响应数据
        return JsonResponse(data=data, status=200, safe=False, json_dumps_params={"ensure_ascii": False})
