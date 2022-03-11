from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve

from mysite import settings
from tracer.views import account, file, setting, issues, project_detail, statistics
from tracer.views import project
from tracer.views import wiki

urlpatterns = [
    path('register/', account.register, name='register'),
    path('register_valid_code/', account.register_valid_code),
    path('login/', account.login, name='login'),
    path('login/sms/', account.login_sms, name='login_sms'),
    path('get_validCode_img/', account.get_validCode_img, name='image_code'),
    path('index/', account.index, name='index'),
    re_path('^$', account.index),
    path('logout/', account.logout, name='logout'),
    re_path(r"media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    # path('upload/', account.upload),
    #项目列表
    path('project/list/', project.project_list, name='project_list'),
    re_path(r'^project/list/application/(?P<project_id>\d+)/$', project.project_application, name='project_application'),
    # /project/star/my/1
    # /project/star/join/1
    re_path(r'^project/unstar/(?P<project_type>\w+)/(?P<project_id>\d+)/$', project.project_unstar, name='project_unstar'),
    re_path(r'^project/star/(?P<project_type>\w+)/(?P<project_id>\d+)/$', project.project_star, name='project_star'),

    #项目管理
    re_path(r'^manage/(?P<project_id>\d+)/', include([
        re_path(r'^wiki/$', wiki.wiki, name='wiki'),
        re_path(r'^wiki/add/$', wiki.wiki_add, name='wiki_add'),
        re_path(r'^wiki/catalog/$', wiki.wiki_catalog, name='wiki_catalog'),
        # re_path(r'^wiki/sub/catalog/(?P<wiki_id>\d+)/$', wiki.wiki_sub_catalog, name='wiki_sub_catalog'),
        re_path(r'^wiki/delete/(?P<wiki_id>\d+)/$', wiki.wiki_delete, name='wiki_delete'),
        re_path(r'^wiki/edit/(?P<wiki_id>\d+)/$', wiki.wiki_edit, name='wiki_edit'),
        re_path(r'^wiki/upload/$', wiki.wiki_upload, name='wiki_upload'),

        re_path(r'^file/$', file.file, name='file'),
        re_path(r'^file/delete/$', file.file_delete, name='file_delete'),
        re_path(r'^cos/credential/$', file.cos_credential, name='cos_credential'),
        re_path(r'^file/post/$', file.file_post, name='file_post'),
        re_path(r'^file/download/(?P<file_id>\d+)/$', file.file_download, name='file_download'),

        re_path(r'^setting/$', setting.setting, name='setting'),
        re_path(r'^setting/delete/$', setting.delete, name='setting_delete'),

        re_path(r'^issues/$', issues.issues, name='issues'),
        re_path(r'^issues/detail/(?P<issues_id>\d+)/$', issues.issues_detail, name='issues_detail'),
        re_path(r'^issues/record/(?P<issues_id>\d+)/$', issues.issues_record, name='issues_record'),
        re_path(r'^issues/change/(?P<issues_id>\d+)/$', issues.issues_change, name='issues_change'),
        re_path(r'^issues/invite/url/$', issues.invite_url, name='invite_url'),

        re_path(r'^project/detail/$', project_detail.project_detail, name='project_detail'),
        re_path(r'^dashboard/issues/chart/$', project_detail.issues_chart, name='issues_chart'),
        re_path(r'^project/test_result/$', project_detail.test_result, name='test_result'),

        re_path(r'^statistics/$', statistics.statistics, name='statistics'),
        re_path(r'^statistics/priority/$', statistics.statistics_priority, name='statistics_priority'),
        re_path(r'^statistics/project/user/$', statistics.statistics_project_user, name='statistics_project_user'),

    ], None)),

]