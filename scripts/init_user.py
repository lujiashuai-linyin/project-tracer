import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault('DJANGON_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from tracer import models

models.UserInfo.objects.create(username='卢嘉帅', email='690067698@qq.com', telephone='13763430435', password='xianjian1998')