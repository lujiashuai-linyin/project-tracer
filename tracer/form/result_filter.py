from django import forms
from django.core.exceptions import ValidationError

from tracer import models
from tracer.form.widgets import ColorRadioSelect
from tracer.form.bootstrap import BootStrapForm

class ResultFilter(BootStrapForm, forms.ModelForm):
    datetime = forms.DateTimeField(label='收录时间')
    result = forms.ChoiceField(choices=(('', '请选择'), ('1', 'Yes'), ('0', 'No')))
    class Meta:
        model = models.TikTokAutoTest
        fields = ['platform', 'version_detail', 'task_id', 'test_path', 'event', 'test_case_url', 'result']
        widgets = {
            'result': forms.Select(attrs={"title": "请选择", 'class': "selectpicker", "data-live-search": "true", "data-dropup-auto": "false"}),
            "datetime": forms.DateTimeInput(attrs={"title": "请选择", 'autocomplete': "off"}),
        }
