from django import forms
from django.core.exceptions import ValidationError

from tracer import models
from tracer.form.widgets import ColorRadioSelect
from tracer.form.bootstrap import BootStrapForm

class ResultFilter(forms.ModelForm):
    datetime = forms.DateTimeField(label='收录时间', widget=forms.DateTimeInput)
    result = forms.ChoiceField(choices=(('', 'None'), ('1', 'Yes'), ('0', 'No')))
    class Meta:
        model = models.TikTokAutoTest
        fields = ['platform', 'version_detail', 'task_id', 'test_path', 'event', 'test_case_url', 'result']
        widgets = {
            'platform': forms.NullBooleanSelect(attrs={}),
            'result': forms.RadioSelect(attrs={})
        }
