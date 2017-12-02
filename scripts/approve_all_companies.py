import os, sys
proj_path = "/home/tomek/pracr/"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pracr.settings')
sys.path.append(proj_path)
import pracr.wsgi
import datetime

from reviews.models import Company
from users.models import User

companies = Company.objects.all()
reviewer = User.objects.get(email="tmierz@rocketmail.com")

for company in companies:
    company.approved = True
    company.reviewer = reviewer
    company.reviewed_date = datetime.datetime.now()
    company.save()
