from django.shortcuts import render

from tracer.serializers import SceneInfoModelSerializer
from rest_framework.viewsets import ModelViewSet
from tracer.models import SceneInfo
class SceneInfoViewSet(ModelViewSet):
    queryset = SceneInfo.objects.all()
    serializer_class = SceneInfoModelSerializer

def mock_scene(request, project_id):
    queryset = SceneInfo.objects.all()
    tot = queryset.count()
    return render(request, "mock_scene.html", {"scene_object_list": queryset, "tot":tot})