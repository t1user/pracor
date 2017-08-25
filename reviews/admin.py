from django.contrib import admin
from .models import Company, Review, Salary, Position


myModels = [Company, Review, Salary, Position]

admin.site.register(myModels)
