from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.db import models
from django.forms import Textarea, TextInput
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
    readonly_fields = ('items',)

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
    model = Visit
    classes = ('collapse',)
    raw_id_fields = ('company',)
    extra = 0
    readonly_fields = ('timestamp', 'company')


class ProfileInline(admin.StackedInline):
    model = Profile
    radio_fields = {'sex': admin.HORIZONTAL}
    fieldsets = (
        (None, {
            'fields': ('contributed', 'sex', 'career_start_year',)
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

    list_display = ('email', 'first_name', 'last_name',
                    'get_contributed', 'last_login', 'get_social', 'is_staff',)
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    def get_contributed(self, obj):
        return obj.profile.contributed
    get_contributed.short_description = "Zrobił wpis"

    def get_social(self, obj):
        return UserSocialAuth.objects.get(user=obj).provider
    get_social.short_description = "login zewnętrzny"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    For benefit of editors who do not have permission to edit users.
    """
    readonly_fields = ('user', 'date_joined',
                       'last_login', 'visited_companies')
    list_display = ('user', 'sex', 'date_joined', 'last_login', 'contributed')
    inlines = (VisitInline,)
    radio_fields = {'sex': admin.HORIZONTAL}
    fieldsets = (
        (None, {
            'fields': (('user', 'contributed'), 'sex', 'career_start_year',)
        }),
        (None, {
            'fields': ('date_joined', 'last_login',)
        }),
        ('Pola linkedin', {
            'classes': ('collapse',),
            'fields': ('linkedin_id', 'linkedin_url'),
        }),
        (None, {
            'classes': ('collapse',),
            'fields': ('visited_companies',),
        }),

    )

    def date_joined(self, obj):
        return obj.user.date_joined
    date_joined.short_description = "data dołączenia"

    def last_login(self, obj):
        return obj.user.last_login
    last_login.short_description = "ostatnie logowanie"
