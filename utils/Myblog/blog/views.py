import os

from bs4 import BeautifulSoup

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, F
from django.db.models.functions import TruncMonth
from django.shortcuts import render, HttpResponse, redirect

from django.http import JsonResponse
from django.contrib import auth
# Create your views here.
from django.views.decorators.clickjacking import xframe_options_sameorigin

from Myblog import settings
from blog.Myforms import UserForm
from blog.models import UserInfo
from blog import models


def login(request):

    if request.method == "POST":

        response = {"user":None, "msg":None}
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        valid_code = request.POST.get("valid_code")

        valid_code_str = request.session.get("valid_code_str")
        if valid_code.upper() == valid_code_str.upper():
            user = auth.authenticate(username = user, password = pwd)
            if user:
                auth.login(request, user)#request.user == 当前登录对象
                response["user"]=user.username
            else:
                response["msg"]="用户名或密码错误"
        else:
            response["msg"]="验证码错误"

        return JsonResponse(response)

    return render(request, 'login.html')

def get_validCode_img(request):
    '''
    基于PIL模块生成响应状态图片
    :param request:
    :return:
    '''
    from blog.utils.validCode import get_validCode_img
    img_data=get_validCode_img(request)
    return HttpResponse(img_data)

def index(request):

    article_list = models.Article.objects.all()

    return render(request, "index.html", {"article_list":article_list})

def logout(request):
    print("sdsdsd")

    # auth.logout(request)
    request.session.flush()

    return redirect('/login/')


def register(request):
    if request.method == "POST":#也可以request.is_ajax():
        print(request.POST)
        form = UserForm(request.POST)

        response = {"user":None, "msg":None}
        if form.is_valid():
            response["user"] = form.cleaned_data.get("user")
            user = form.cleaned_data.get("user")
            pwd = form.cleaned_data.get("pwd")
            email = form.cleaned_data.get("email")
            avatar_obj = request.FILES.get("avatar")

            extra = {}
            if avatar_obj:
                extra["avatar"] = avatar_obj
                user_obj = UserInfo.objects.create_user(username=user, password=pwd, email=email, **extra)

        else:
            print(form.cleaned_data)
            print(form.errors)
            response["msg"] = form.errors

        return JsonResponse(response)

    form = UserForm()

    return render(request, "register.html", {"form":form})

def home_site(request, username, **kwargs):
    '''
    个人站点试图函数
    :param request:
    :param username:
    :return:
    '''
    print("username", username)
    user = UserInfo.objects.filter(username=username).first()
    #判断用户是否存在
    if not user:
        return render(request, "not_found.html")

    #查询当前站点对象
    blog = user.blog
    #当前站点或用户对应的所有文章
    #基于对象查询
    # article_list = user.article_set.all()
    #基于双下划线

    if kwargs:
        condition = kwargs.get("condition")
        param = kwargs.get("param")

        if condition == "category":

            article_list = models.Article.objects.filter(user=user).filter(category__title=param)

    else:

        article_list = models.Article.objects.filter(user=user)
    #每一个后的表模型.object.value('pk').annotate(聚合函数(关联表__统计字段)).values("表模型的所有字段")
    #查询每一个分类名称及对应的文章数
    # ret = models.Category.objects.values('pk').annotate(c=Count("article__title")).values('title', "c")
    # print(ret)

    #查询当前站点每一个分类名称对应的文章数
    # cate_list = models.Category.objects.filter(blog=blog).values('pk').annotate(c=Count("article__title")).values_list('title', "c")
    # print(cate_list)

    #查询当前站点每一个标签名称对应的文章数
    # tag_list = models.Tag.objects.filter(blog=blog).values('pk').annotate(c=Count("article")).values_list("title", "c")
    # print(tag_list)
#查询当前站点每一个年月名称对应的文章数
    #额外的sql注入
    # ret = models.Article.objects.extra(select={"is_recent": "create_time > '2021-12-26'"}).values("title", "is_recent")
    # print(ret)
    #方式一
    # date_list = models.Article.objects.filter(user=user).extra(select={"y_m_date": "date_format(create_time, '%%Y-%%m')"}).values_list('y_m_date').annotate(c=Count("nid")).values_list("y_m_date", "c")
    # print(date_list)
    # 方式二
    #TruncMonth方法
    # date_list = models.Article.objects.filter(user=user).annotate(month=TruncMonth('create_time')).values("month").annotate(c=Count("nid")).values("month", "c")

    return render(request, "home_site.html", {"username": username, "blog": blog, "article_list": article_list})

def get_classification_data(username):
    user = UserInfo.objects.filter(username=username).first()

    blog = user.blog

    cate_list = models.Category.objects.filter(blog=blog).values('pk').annotate(c=Count("article__title")).values_list('title', "c")

    tag_list = models.Tag.objects.filter(blog=blog).values('pk').annotate(c=Count("article")).values_list("title", "c")

    date_list = models.Article.objects.filter(user=user).extra(select={"y_m_date": "date_format(create_time, '%%Y-%%m')"}).values_list('y_m_date').annotate(c=Count("nid")).values_list("y_m_date", "c")

    return {"cate_list": cate_list, "blog": blog, "tag_list": tag_list, "date_list": date_list}

def article_detail(request, username, article_id):
    user = UserInfo.objects.filter(username=username).first()
    #判断用户是否存在
    if not user:
        return render(request, "not_found.html")

    blog = user.blog

    article_obj = models.Article.objects.filter(pk=article_id).first()

    comment_list = models.Comment.objects.filter(article_id=article_id)


    return render(request, "article_detail.html", locals())

#点赞试图函数
import json
def digg(request):

    print(request.POST)

    article_id = request.POST.get("article_id")
    is_up = json.loads(request.POST.get("is_up"))#"true"需要反序列化

    user_id = request.user.pk

    obj = models.ArticleUpDown.objects.filter(user_id=user_id, article_id=article_id).first()
    response = {"state":True}
    if not obj:
        ard = models.ArticleUpDown.objects.create(user_id=user_id, article_id=article_id, is_up=is_up)
        queryset = models.Article.objects.filter(pk=article_id)
        if is_up:
            queryset.update(up_count=F("up_count")+1)
        else:
            queryset.update(down_count=F("down_count")+1)
    else:
        response["state"] = False
        response["handled"] = obj.is_up

    return JsonResponse(response)

def comment(request):
    print(request.POST)
    article_id = request.POST.get("article_id")
    pid = request.POST.get("pid")
    content = request.POST.get("content")
    user_id = request.user.pk

    article_obj= models.Article.objects.filter(pk=article_id).first()
    response = {}
    with transaction.atomic():
        comment_obj = models.Comment.objects.create(user_id=user_id,article_id=article_id,content=content,parent_comment_id=pid)
        models.Article.objects.filter(pk=article_id).update(comment_count=F("comment_count")+1)
    if pid:
        parent_comment_obj = comment_obj.parent_comment
        response["parent_comment_user"]=parent_comment_obj.user.username
        response["parent_comment_content"]=parent_comment_obj.content

    content=comment_obj.content

    response["create_time"]=comment_obj.create_time.strftime("%Y-%m-%d %X")
    response["username"]=request.user.username
    response["content"]=content
    response["comment_pk"]=comment_obj.pk


    #发送文件

    from django.core.mail import send_mail
    from Myblog import settings

    # send_mail(
    #     "您的文章%s新增了一条评论"%article_obj.title,
    #     content,
    #     settings.EMAIL_HOST_USER,
    #     ["690067698@qq.com"]
    #
    # )
    # import threading
    # t = threading.Thread(target=send_mail, args=("您的文章%s新增了一条评论"%article_obj.title,
    #                                          content,
    #                                          settings.EMAIL_HOST_USER,
    #                                          ["690067698@qq.com",]))
    # t.start()


    return JsonResponse(response)

def get_comment_tree(request):

    article_id = request.GET.get("article_id")
    ret = list(models.Comment.objects.filter(article_id=article_id).order_by("pk").values("pk","content","parent_comment_id"))
    return JsonResponse(ret, safe=False)

@login_required
def my_backend(request):

    article_list = models.Article.objects.filter(user=request.user)

    return render(request,"backend/backend.html", locals())

@login_required
def add_article(request):

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        soup = BeautifulSoup(content,"html.parser")
        #过滤
        for tag in soup.find_all():
            if tag.name=="script":
                tag.decompose()

        #获取文本进行截取

        desc = soup.test[0:150]
        models.Article.objects.create(title=title,desc=desc, content=content,user=request.user)
        return redirect("/my_backend/")
    return render(request, "backend/add_article.html")

from django.http import HttpResponse
@xframe_options_sameorigin
def upload(request):
    print(request.FILES)
    img=request.FILES.get("upload_img")
    path = os.path.join(settings.MEDIA_ROOT,"add_article_img",img.name)
    with open(path,"wb") as f:
        for line in img:
            f.write(line)


    response={
        "error":0,
        "url":"/media/add_article_img/%s"%img.name
    }

    import json

    return HttpResponse(json.dumps(response))