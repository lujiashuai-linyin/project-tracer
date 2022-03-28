import sys
import json
import requests
try:
    export_user = sys.argv[1]
except:
    print ('需要命令行输入用户邮箱前缀')
    exit()
res_list = []
try:
    case_list = [x.strip() for x in open("./case_list.txt").readlines()]
except:
    print ('没有找到case 文件')
    exit()
u = "https://ies-qa-bsqa.bytedance.net/api/v2/bsqa_api"
post_data = {'url': 'et_case_export'}
post_data['export_user'] = export_user
post_data['case_list'] = case_list
r = requests.post(u, data=json.dumps(post_data))