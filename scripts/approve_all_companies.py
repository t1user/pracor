import os
import sys


import getpass
user = getpass.getuser()
proj_path = "/home/" + user + "/pracr/"

sys.path.append(proj_path)
import pracr.wsgi
import datetime

from reviews.models import Company
from users.models import User

companies = Company.objects.all()
reviewer = User.objects.get(email="tmierz@rocketmail.com")

companies.update(
    approved=True,
    reviewer=reviewer,
    reviewed_date=datetime.datetime.now()
)

"""
for company in companies:
    company.approved = True
    company.reviewer = reviewer
    company.reviewed_date = datetime.datetime.now()
    company.save()
"""
