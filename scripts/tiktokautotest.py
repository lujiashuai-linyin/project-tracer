from scripts import base
from tracer import models
def run():
    models.TikTokAutoTest.objects.filter(platform='Android').update(platform=1)
if __name__ == "__main__":
    run()
