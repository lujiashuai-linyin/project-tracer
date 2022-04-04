import os
import sys
import django
import requests

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from tracer import models

# models.PricePolicy.objects.create(category=3, title='字节专用版', price=100000, project_num=20, project_member=2000, project_space=10, per_file_size=2048, )
# case_list = models.TikTokAutoTest.objects.filter(project_id=10, task_id=0)
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

from datetime import datetime
now_weekday = datetime.today().isoweekday()
if now_weekday in [1, 2, 6, 7]:
    print('回归')
elif now_weekday == 3:
    print('一灰')
elif now_weekday == 4:
    print('二灰')
else:
    print('三灰')


