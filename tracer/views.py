from django.http import JsonResponse
from django.shortcuts import render
from tracer.my_forms import UserForm

def register(request):
    if request.method == 'POST':
        print(request.POST)
        form = UserForm(request.POST)

        response = {'user': None, 'msg': None}
        if form.is_valid():
            print(form.cleaned_data)
            response['user'] = form.cleaned_data.get('user')
            user = form.cleaned_data.get("user")
            pwd = form.cleaned_data.get('pwd')
            email = form.cleaned_data.get('email')
            telephone = form.cleaned_data.get('telephone')
            avatar_obj = request.FILES.get('avatar')

            extra = {}
            if avatar_obj:
                extra['avatar'] = avatar_obj
                user_obj = UserForm.objects.create_user(username=user, password=pwd, email=email, telephone=telephone, **extra)

        else:
            print(form.cleaned_data)
            print(form.errors)
            response['msg'] = form.errors

        return JsonResponse(response)
