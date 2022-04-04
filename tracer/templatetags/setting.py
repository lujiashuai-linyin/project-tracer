from django.template import Library

register = Library()

@register.inclusion_tag('inclusion/setting_list.html')
def setting_base_list(request):

    return {'status': True, 'request': request}