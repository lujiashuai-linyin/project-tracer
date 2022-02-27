from django.shortcuts import render


def project_detail(request, project_id):
    return render(request, 'project_detail.html')
def issues_chart(request):
    pass