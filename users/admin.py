from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import Profile

from .models import User



class ProfileInline(admin.StackedInline):
    model = Profile
    radio_fields = {'sex': admin.HORIZONTAL}
    fieldsets = (
        (None, {
            'fields': ( 'contributed', 'sex', 'career_start_year',)
            }),
        ('Pola linkedin', {
            'classes': ('collapse',),
            'fields': ('linkedin_id', 'linkedin_url'),
            }),
        )


    

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    inlines = (ProfileInline, )

    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {
            'classes': ('collapse',),
            'fields': ('first_name', 'last_name',)}),
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

    list_display = ('email', 'first_name', 'last_name', 'is_staff',)
    search_fields = ( 'email', 'first_name', 'last_name')
    ordering = ('email',)

"""
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('user',)
    radio_fields = {'sex': admin.HORIZONTAL}
    fieldsets = (
        (None, {
            'fields': (('user', 'contributed'), 'sex', 'career_start_year',)
            }),
        ('Pola linkedin', {
            'classes': ('collapse',),
            'fields': ('linkedin_id', 'linkedin_url'),
            }),
        )



"""
