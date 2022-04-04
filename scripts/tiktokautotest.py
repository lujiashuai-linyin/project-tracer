import requests

from scripts import base
from tracer import models
def run():
    res = requests.get(url='http://demo.finereport.com/', )
    with open('../detector/templates/detector/login.html', 'w', encoding='utf-8') as f:
        f.write(res.text)
# models.IssuesReply.objects.create(issues_id=1, reply_type=2, content='回复m', creator_id=5, reply_id=1)
if __name__ == "__main__":
    run()
