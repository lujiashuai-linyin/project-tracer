import ssl
import requests
from rest_framework import serializers
from tracer.models import SceneInfo


ssl._create_default_https_context = ssl._create_unverified_context

class SceneInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SceneInfo
        fields = ['platform', 'scene_id', "test_path", 'scene_path', 'create_time']
        extra_kwargs = {
            "create_time":{
                "read_only":True,
            }
        }

    def validate(self, attrs):
        scene_id = attrs.get('scene_id', 0)
        platform = attrs.get('platform', -1)
        exist = SceneInfo.objects.filter(scene_id=scene_id, platform=platform).exists()
        if exist:
            raise serializers.ValidationError('场景已存在')
        if platform == -1:
            raise serializers.ValidationError('平台输入错误')
        return attrs
