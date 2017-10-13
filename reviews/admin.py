from django.contrib import admin
from .models import Company, Review, Salary, Position, Interview


myModels = [Review, Salary, Position, Interview]

admin.site.register(myModels)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    readonly_fields = ('overallscore', 'advancement', 'worklife', 'compensation',
                       'environment', 'number_of_reviews')
    actions = ['update_scores']
    search_fields = ['name']
    
    fieldsets = (
        (None, {
            'fields': ('name', ('headquarters_city', 'website'), )
                       }),
         ('Dodatkowe informacje', {
             'classes': (),
             'fields': ('region', 'country', 'employment', 'public', 'ownership')
             }),
         ('Oceny', {
             'classes': ('collapse',), 
             'fields': ('overallscore', 'advancement', 'worklife', 'compensation',
                         'environment', 'number_of_reviews')
             }),
         )

    def update_scores(self, request, queryset):
        for item in queryset:
            item.update_scores()
    update_scores.short_description = "Uaktualnij oceny"
            
