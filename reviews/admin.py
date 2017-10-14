from django.contrib import admin
from django.db import models
from django.forms import Textarea, TextInput
from .models import Company, Review, Salary, Position, Interview

admin.site.site_header = 'pracr - administracja'

myModels = [Position, Interview]

admin.site.register(myModels)

class ModelAdminModified(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        """Adds user as reviewer if the instance has been approved."""
        if obj.approved == True and not obj.reviewer:
            obj.reviewer = request.user
        super().save_model(request, obj, form, change)



class ReviewInline(admin.TabularInline):
    model = Review
    classes = ('collapse',)
    extra = 0

class SalaryInline(admin.TabularInline):
    model = Salary
    classes = ('collapse',)
    extra = 0

class InterviewInline(admin.TabularInline):
    model = Interview
    classes = ('collapse',)
    extra = 0

@admin.register(Company)
class CompanyAdmin(ModelAdminModified):
    readonly_fields = ('overallscore', 'advancement', 'worklife', 'compensation',
                       'environment', 'number_of_reviews', 'reviewer')
    actions = ['update_scores']
    search_fields = ['name']
    list_display = ['name', 'headquarters_city', 'website', 'number_of_reviews',
                    'approved', 'reviewer']
    inlines = (ReviewInline, SalaryInline, InterviewInline, )
    list_filter = ('approved', )
    
    fieldsets = (
        (None, {
            'fields': ('name', ('headquarters_city', 'website'), )
                       }),
         ('Dodatkowe informacje', {
             'classes': ('collapse',),
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

@admin.register(Review)
class ReviewAdmin(ModelAdminModified):
    list_filter = ('approved',)
    list_display = ('id', 'title', 'company', 'approved', 'reviewer')
    list_display_links = ('id', 'title',)
    readonly_fields = ('date', 'id', 'reviewer')
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': 60})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':60})}
        }
    
@admin.register(Salary)
class SalaryAdmin(ModelAdminModified):
    readonly_fields = ('date', 'company', 'position', 'base_monthly',
                       'base_annual', 'total_monthly', 'total_annual', 'reviewer',)
    list_filter = ('approved', 'reviewer')
    fieldsets = (
        (None, {
            'fields': ('date', 'company', 'position','currency',),
            }),
         ('Dane wprowadzone', {
             'fields': (('salary_input', 'period','gross_net'),
                       ('bonus_input', 'bonus_period', 'bonus_gross_net')),
            }),
         ('Dane wyliczone', {
             'fields': (('base_monthly', 'base_annual',), ('total_monthly', 'total_annual'))
             }),
         )
"""    
@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    radio_fields = {'got_offer': admin.HORIZONTAL}
"""

@admin.register(admin.models.LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('get_change_message', 'object_repr', 'action_time', 'user', 'action_flag')
    list_filter = ('user',)


