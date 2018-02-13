from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils import six, timezone
from django.utils.translation import ugettext_lazy as _

from reviews.models import Company


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self,  email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.

        Username has been removed from the original class implementation.

        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        # take out userename if it's added by social-auth (modification from
        # original method)
        if 'username' in extra_fields:
            del extra_fields['username']
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom user model that substitutes username for email."""
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Profile(models.Model):
    year = timezone.now().year
    SEX = [('K', 'Kobieta'), ('M', 'Mężczyzna')]
    career_year = range(year, 1959, -1)
    CAREER_YEAR = [(i, i) for i in career_year]
    EDU = [
        ('A', 'wyższe'),
        ('A0', 'student'),
        ('A1', 'MBA'),
        ('A2', 'stopień naukowy'),
        ('A3', 'inne podyplomowe'),
        ('B', 'średnie'),
        ('C', 'gimnazjalne'),
        ('D', 'zasadnicze'),
        ('E', 'podstawowe'),
        ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, editable=False)
    #default True, because if logged in by SocialAuth no confirmation neccessary
    email_confirmed = models.BooleanField('Potwierdzony email', default=True)
    contributed = models.BooleanField('Zrobił wpis', default=False)
    sex = models.CharField("płeć", max_length=1, choices=SEX, default=None,
                           null=True, blank=True)
    career_start_year = models.PositiveIntegerField("rok rozpoczęcia kariery",
                                                    choices=CAREER_YEAR,
                                                    null=True, blank=True)
    education = models.CharField("wykształcenie",
                                 max_length=2, choices=EDU, default=None,
                                 blank=True, null=True)
    linkedin_id = models.CharField(max_length= 10, null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    visited_companies = models.ManyToManyField(Company, through='Visit')

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profil"
    
    def __str__(self):
        return self.user.email


class Visit(models.Model):
    company = models.ForeignKey(Company)
    user = models.ForeignKey(Profile)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=True,
                                      editable=False, blank=True, null=True)
    path = models.CharField(max_length=100, editable=False)

    class Meta:
        verbose_name = 'Wizyta'
        verbose_name_plural = 'Wizyty'
    
    def __str__(self):
        return self.company.name
