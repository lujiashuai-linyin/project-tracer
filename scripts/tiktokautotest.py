from scripts import base
from tracer import models
def run():
    models.IssuesReply.objects.create(issues_id=1, reply_type=2, content='回复m', creator_id=5, reply_id=1)
if __name__ == "__main__":
    run()
