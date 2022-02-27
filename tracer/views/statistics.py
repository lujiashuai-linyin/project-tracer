from django.shortcuts import render


def statistics(request, project_id):
    return render(request, 'statistics.html')
def statistics_priority(request, project_id):
    pass
def statistics_project_user(request):
    pass