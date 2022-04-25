from django.db import models

# Create your models here.
class Student(models.Model):
    """
    学生表
    """
    SEX_CHOICE = [
        (0, "男"),
        (1, "女")
    ]
    name = models.CharField(verbose_name="姓名", max_length=16)
    sex = models.SmallIntegerField(verbose_name="性别", choices=SEX_CHOICE)
    age = models.PositiveIntegerField(verbose_name="年龄")
    classmate = models.CharField(verbose_name="班级", max_length=12)
    discription = models.TextField(verbose_name="个性签名", max_length=32, null=True, blank=True)
    create_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        index_together = ['id', 'create_at']
        ordering = ('id', "-create_at")