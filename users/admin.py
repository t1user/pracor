from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.db import models
from django.forms import Textarea, TextInput
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from social_django.models import UserSocialAuth

from reviews.models import Interview, Position, Review, Salary

from .models import Profile, User, Visit


class SocialDjangoInline(admin.StackedInline):
    model = UserSocialAuth
    extra = 0
    readonly_fields = ('user', 'provider', 'uid', 'extra_data')
    list_filter = ('provider',)

    def has_add_permission(self, request):
        return False

    
class PositionInline(admin.StackedInline):
    model = Position
    extra = 0
    raw_id_fields = ('company',)
    show_change_link = True
    readonly_fields = ('items', 'date')
    list_select_related = True

    def items(self, obj):
        review = Review.objects.filter(position=obj)
        salary = Salary.objects.filter(position=obj)
        if review:
            review=' opinia: {}'.format(review[0])
        else:
            review=''
        if salary:
            salary=' zarobki: {}'.format(salary[0])
        else:
            salary=''
        return str(review) + str(salary)

    
class InterviewInline(admin.TabularInline):
    model = Interview
    extra = 0
    fk_name = 'user'
    raw_id_fields = ('company',)
    show_change_link = True

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': 20})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 20})}
    }

    
class VisitInline(admin.TabularInline):
    """
    CURRENTLY NOT IN USE.
    SQL query is very slow.
    """
    model = Visit
    classes = ('collapse',)
    raw_id_fields = ('company',)
    extra = 0
    readonly_fields = ('timestamp', 'company', 'path', 'ip')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related()
        return qs


class ProfileInline(admin.StackedInline):
    model = Profile
    radio_fields = {'sex': admin.HORIZONTAL}
    readonly_fields = ('id',)
    can_delete = False
    fieldsets = (
        (None, {
            'fields': ('contributed', 'email_confirmed', 'sex', 'career_start_year', 'id')
        }),
        ('Pola linkedin', {
            'classes': ('collapse',),
            'fields': ('linkedin_id', 'linkedin_url'),
            }),
    )
    list_filter = ('contributed',)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    inlines = (ProfileInline, SocialDjangoInline, PositionInline, InterviewInline)
    readonly_fields = ('last_login', 'date_joined', 'id')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'id')}),
        (_('Permissions'), {
            'classes': ('collapse',),
            'fields': ('is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    list_display = ('email', 'id', 'first_name', 'last_name',
                    'get_contributed', 'last_login', 'get_social', 'is_staff',)
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    def get_contributed(self, obj):
        return obj.profile.contributed
    get_contributed.short_description = "Zrobił wpis"

    def get_social(self, obj):
        return ', '.join([a.provider for a in UserSocialAuth.objects.filter(user=obj)])
    get_social.short_description = "login zewnętrzny"

    def get_inline_instances(self, request, obj=None):
        """
        Ensure Profile instance is not available while user is created
        (because the signal to create Profile hasn't been sent yet,
        so Profile doesn't exist).
        """
        if not obj:
            return []
        return super().get_inline_instances(request, obj)
        

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    For benefit of editors who do not have permission to edit users.
    """
    readonly_fields = ('user', 'date_joined',
                       'last_login', 'show_visits', 'show_unique_visits')
    list_display = ('user', 'sex', 'date_joined', 'last_login', 'contributed',)
    radio_fields = {'sex': admin.HORIZONTAL}
    
    fieldsets = (
        (None, {
            'fields': (('user', 'contributed', 'email_confirmed'), 'sex', 'career_start_year',
                       'education')
        }),
        (None, {
            'fields': ('date_joined', 'last_login',)
        }),
        ('Pola linkedin', {
            'classes': ('collapse',),
            'fields': ('linkedin_id', 'linkedin_url'),
        }),
        ('Wizyty', {
            'classes': ('collapse',),
            'fields': ('show_visits',),
        }),
        ('Odwiedzone firmy', {
            'classes': ('collapse',),
            'fields': ('show_unique_visits',),
        }),
    )

    def date_joined(self, obj):
        return obj.user.date_joined
    date_joined.short_description = "data dołączenia"

    def last_login(self, obj):
        return obj.user.last_login
    last_login.short_description = "ostatnie logowanie"

    def show_visits(self, obj):
        """
        Provide visit information in no more than 2 queries (inlines suffer from n+1 issue).
        """
        visits = obj.visited_companies.through.objects.filter(
            user=obj).order_by(
                '-timestamp').values(
                    'timestamp',
                    'company__name',
                    'path',
                    'ip', )
        count = visits.count()
        display = [['{:%d/%m/%y %H:%M}'.format(timezone.localtime(item['timestamp'])),
                    item['company__name'],
                    item['path'],
                    str(item['ip'] or " ")]
                   for item in visits]
        display = '\n'.join('\t'.join(i) for i in display)
        display = 'Liczba wizyt: {}\n'.format(count) + display
        return display
    show_visits.short_description = "wizyty"


    def show_unique_visits(self, obj):
        """
        List all visited Companies with number of visits for each.
        """
        visits = obj.visited_companies.values('name').annotate(models.Count('name'))
        display = [[item['name'], str(item['name__count'])] for item in visits]
        display = '\n'.join(' - '.join(i) + 'x' for i in display)
        display = 'Odwiedzonych firm: {}\n'.format(visits.count()) + display
        return display
    show_unique_visits.short_description = "odwiedzone firmy"

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    readonly_fields = ('company', 'user', 'timestamp', 'ip', 'path')
    list_display =  ( 'timestamp', 'company', 'user', 'path', 'ip')
    search_fields = ('company__name', 'company__slug', 'company__website', 'user__user__email', )
    list_filter = ('timestamp', 'ip')
    
