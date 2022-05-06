import os
import sys
import django
import requests
from django.db.models import Count

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from tracer import models

# models.PricePolicy.objects.create(category=3, title='字节专用版', price=100000, project_num=20, project_member=2000, project_space=10, per_file_size=2048, )
case_list = models.UserInfo.objects.filter(create_time__gte='2022-04-25')
print(case_list)
# result=[]
# for case_id in case_list:
#     result.append(case_id.case_id)
# with open('result.txt', 'w') as f:
#     f.write(str(result))
# response = requests.get(url='https://cony.bytedance.net/calendar/tiktok')
# with open('version.html', 'w') as f:
#     f.write(response.text)

# import sys
# import json
# import requests
# try:
#     export_user = sys.argv[1]
# except:
#     # print ('需要命令行输入用户邮箱前缀')
#     # exit()
#     pass
# res_list = []
# case_list = []
# try:
#     case_list = ["406113", "405112"]
#     # case_list = [x.strip() for x in open("./case_list.txt").readlines()]
# except:
#     print ('没有找到case 文件')
#     exit()
# u = "https://ies-qa-bsqa.bytedance.net/api/v2/bsqa_api"
# post_data = {'url': 'et_case_export'}
# post_data['export_user'] = "lujiashuai.777"
# post_data['case_list'] = case_list
# print(case_list)
# r = requests.post(u, data=json.dumps(post_data))
# print(r.text)

# response = requests.get(url='https://cony.bytedance.net/api/calendar', params={'space_alias': 'tiktok'}, headers={'content-type': 'application/json'})

# project_object = models.Project.objects.count()
# print(project_object)

# def chose_string(source, target):
#     n = len(source)
#     m = len(target)
#     if m == 0:
#         return 0
#     if m > n:
#         return -1
#     for i in range(n - m + 1):
#         k = i
#         for j in range(m):
#             if source[k] == target[j]:
#                 if j == m-1:
#                     return i
#                 k += 1
#             else:
#                 break
#         return -1
