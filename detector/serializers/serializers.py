from rest_framework import serializers
from detector import models

class StudentModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        # fields = "__all__"
        fields = ['name', 'age', 'sex']

class Student1Serializers(serializers.Serializer):
    """学生信息序列化器"""
    # 转化字段声明
    id = serializers.IntegerField()
    name = serializers.CharField()
    sex = serializers.BooleanField()
    age = serializers.IntegerField()
    discription = serializers.CharField()