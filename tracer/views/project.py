from django.shortcuts import render

def project_list(request):
    # print(request.tracer.user.username)
    # print(request.price_policy.project_member)
    return render(request, 'project_list.html')