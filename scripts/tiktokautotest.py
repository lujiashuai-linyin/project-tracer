from scripts import base
from tracer import models
def run():
    models.TikTokAutoTest.objects.filter(version_detail='V23.5-三灰').delete()
if __name__ == "__main__":
    run()
