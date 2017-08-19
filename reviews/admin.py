from django.contrib import admin
from .models import Company, Review, Salary, Job


myModels = [Company, Review, Salary, Job]

admin.site.register(myModels)
