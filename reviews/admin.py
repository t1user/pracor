from django.contrib import admin
from .models import Company, Review, Salary


myModels = [Company, Review, Salary]

admin.site.register(myModels)


