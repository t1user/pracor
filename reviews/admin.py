from django.contrib import admin
from django.db import models
from django.forms import Textarea, TextInput, RadioSelect
from .models import Company, Review, Salary, Position, Interview
from django.utils import timezone

admin.site.site_header = 'pracr - administracja'

myModels = [Position]

admin.site.register(myModels)

class ModelAdminModified(admin.ModelAdmin):
    list_filter = ('approved',)
    approval = ('Akceptacja', {
        'fields': ('approved', 'reviewer', 'reviewed_date'),
    })

    
    def save_model(self, request, obj, form, change):
        """Adds user as reviewer and review date if the instance has been modified."""
        obj.reviewer = request.user
        obj.reviewed_date = timezone.now()
        super().save_model(request, obj, form, change)

class ItemInline(admin.TabularInline):
    classes = ('collapse',)
    extra = 0
    exclude = ('approved', 'reviewer', 'reviewed_date',)

class ReviewInline(ItemInline):
    model = Review

class SalaryInline(ItemInline):
    model = Salary

class InterviewInline(ItemInline):
    model = Interview

@admin.register(Company)
class CompanyAdmin(ModelAdminModified):
    readonly_fields = ('overallscore', 'advancement', 'worklife', 'compensation',
                       'environment', 'number_of_reviews', 'reviewer', 'date', 'reviewed_date')
    actions = ['update_scores']
    search_fields = ['name']
    list_display = ['name', 'headquarters_city', 'website', 'number_of_reviews',
                    'approved', 'reviewer']
    inlines = (ReviewInline, SalaryInline, InterviewInline, )

    
    fieldsets = (
        (None, {
            'fields': ('name', ('headquarters_city', 'website'),
                       'date',
                       )
                       }),
         ('Dodatkowe informacje', {
             'classes': ('collapse',),
             'fields': ('region', 'country', 'employment', 'public', 'ownership')
             }),
        ModelAdminModified.approval,
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
    list_display = ('id', 'title', 'company', 'approved', 'reviewer')
    list_display_links = ('id', 'title',)
    readonly_fields = ('date', 'id', 'overallscore',
                       'worklife', 'advancement', 'compensation',
                       'environment', 'reviewer', 'reviewed_date', 'company',
                       'position',)
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': 60})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':60})}
        }

    fieldsets = (
        (None, {
            'fields': ('date', 'company', 'position'),
            }),
        (None, {
            'fields': ('title', 'pros', 'cons', 'comment',
                       ('overallscore', 'advancement', 'worklife', 'compensation',
                        'environment',),
                       )}),
        ModelAdminModified.approval,
        )
            
    
@admin.register(Salary)
class SalaryAdmin(ModelAdminModified):
    readonly_fields = ('date', 'company', 'position', 'base_monthly',
                       'base_annual', 'total_monthly', 'total_annual', 'reviewer',
                       'reviewer', 'reviewed_date', 'company', 'position')
    list_display = ('id', 'company', 'approved', 'reviewer')
    search_fields = ['company__name']
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
        ModelAdminModified.approval,
         )
  
@admin.register(Interview)
class InterviewAdmin(ModelAdminModified):
    list_display = ('id', 'company', 'rating', 'approved', 'reviewer')
    list_display_links = ('id', 'company')
    search_fields = ['company__name']
    radio_fields = {'got_offer': admin.HORIZONTAL}
    readonly_fields = ('date', 'company', 'reviewer', 'reviewed_date', 'rating')
    fieldsets = (
        (None, {
            'fields': ('date', 'company', 'position', 'department', 'how_got', 'difficulty',
                       'got_offer', 'questions', 'impressions', 'rating'),}),
        ModelAdminModified.approval,
        )

@admin.register(admin.models.LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('get_change_message', 'object_repr', 'action_time', 'user', 'action_flag')


