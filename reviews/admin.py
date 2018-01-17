from django.contrib import admin
from django.db import models
from django.forms import RadioSelect, Textarea, TextInput, CheckboxSelectMultiple
from django.utils import timezone

from .models import Company, Interview, Position, Review, Salary, Benefit


admin.site.site_header = 'pracor - administracja'

#myModels = [Position]

# admin.site.register(myModels)


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
    exclude = ('reviewer', 'reviewed_date',)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 30})}
    }


class ReviewInline(ItemInline):
    model = Review
    show_change_link = True

class SalaryInline(ItemInline):
    model = Salary
    readonly_fields = ('benefits',)
    show_change_link = True


class InterviewInline(ItemInline):
    model = Interview
    show_change_link = True


@admin.register(Company)
class CompanyAdmin(ModelAdminModified):
    readonly_fields = ('count_reviews', 'count_salaries', 'count_interviews',
                       'reviewer', 'date', 'reviewed_date', 'get_ratings', 'slug')
    actions = ['update_scores']
    search_fields = ['name']
    list_display = ['id', 'name', 'headquarters_city', 'website', 'count_reviews',
                    'count_salaries', 'count_interviews', 'approved', 'reviewer']
    list_display_links = ['name', ]
    inlines = (ReviewInline, SalaryInline, InterviewInline, )

    fieldsets = (
        (None, {
            'fields': ('name', ('headquarters_city', 'website'),
                       'slug', 'date',
                       )
        }),
        ('Dodatkowe informacje', {
            'classes': ('collapse',),
            'fields': (('region', 'country'), 'employment', ('public', 'isin'), 'ownership',
                       'sectors',)
        }),
        ModelAdminModified.approval,
        ('Oceny', {
            'classes': (),
            'fields': (('get_ratings', 'count_reviews'),)
        }),
    )

    def count_reviews(self, obj):
        return obj.reviews.count()
    count_reviews.short_description = "Liczba opinii"

    def count_salaries(self, obj):
        return obj.salaries.count()
    count_salaries.short_description = "Liczba zarobków"

    def count_interviews(self, obj):
        return obj.interviews.count()
    count_interviews.short_description = "Liczba interview"

    def get_ratings(self, obj):
        return obj.get_scores_strings()
    get_ratings.short_description = "Oceny"

    def update_scores(self, request, queryset):
        for item in queryset:
            item.update_scores()
    update_scores.short_description = "Uaktualnij oceny"


@admin.register(Review)
class ReviewAdmin(ModelAdminModified):
    list_display = ('id', 'title', 'company', 'position', 'approved', 'reviewer')
    list_display_links = ('id', 'title',)
    readonly_fields = ('date', 'id', 'overallscore',
                       'worklife', 'advancement', 'compensation',
                       'environment', 'reviewer', 'reviewed_date', 'company',
                       'position',)
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': 60})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 60})}
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
    readonly_fields = ('date', 'company', 'position',
                       'salary_gross_input_period', 'salary_gross_annual',
                       'bonus_gross_input_period', 'bonus_gross_annual',
                       'reviewer', 'reviewed_date',)
    list_display = ('id', 'company', 'position', 'approved', 'reviewer')
    search_fields = ['company__name', 'position__user__email']
    filter_horizontal = ['benefits',]
    fieldsets = (
        (None, {
            'fields': ('date', 'company', 'position', 'currency',),
        }),
        ('Dane wprowadzone', {
            'fields': (('salary_input', 'period', 'gross_net'),
                       ('bonus_input', 'bonus_period', 'bonus_gross_net')),
        }),
        ('Dane wyliczone', {
            'fields': (('salary_gross_input_period', 'salary_gross_annual',),
                       ('bonus_gross_input_period', 'bonus_gross_annual',))
        }),
        ('Benefity', {
            'fields': ('benefits',),
            }),
        ModelAdminModified.approval,
    )
    """formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple() },}"""


@admin.register(Interview)
class InterviewAdmin(ModelAdminModified):
    list_display = ('id', 'company', 'rating', 'user',
                    'got_offer', 'approved', 'reviewer')
    list_display_links = ('id', 'company')
    search_fields = ['company__name']
    radio_fields = {'difficulty': admin.HORIZONTAL}
    readonly_fields = ('date', 'company', 'reviewer',
                       'reviewed_date', 'rating', 'user')
    fieldsets = (
        (None, {
            'fields': ('user', 'date', 'company', 'position', 'department', 'how_got', 'got_offer',
                       'difficulty', 'questions', 'impressions', 'rating'), }),
        ModelAdminModified.approval,
    )


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'position', 'department', 'location', )
    search_fields = ('user__email', 'company__name',)
    inlines = (ReviewInline, SalaryInline)
    readonly_fields = ('user', 'company', 'date')


@admin.register(admin.models.LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('get_change_message', 'object_repr',
                    'action_time', 'user', 'action_flag')

@admin.register(Benefit)
class BenefitAdmin(admin.ModelAdmin):
    
    readonly_fields = ('author', 'reviewed_date')
    list_display = ('name', 'approved', 'reviewer',)
    def save_model(self, request, obj, form, change):
        """Adds user as author of the instance."""
        obj.author = request.user
        super().save_model(request, obj, form, change)

