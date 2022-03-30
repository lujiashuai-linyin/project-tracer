import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from tracer import models

models.PricePolicy.objects.create(category=3, title='字节专用版', price=100000, project_num=20, project_member=2000, project_space=10, per_file_size=2048, )