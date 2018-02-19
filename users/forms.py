from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import PasswordResetForm
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from users.models import User, Profile


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ("email",)
        field_classes = {'email': forms.EmailField}

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        if self._meta.model.EMAIL_FIELD in self.fields:
            self.fields[self._meta.model.EMAIL_FIELD].widget.attrs.update(
                {'autofocus': True})

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        password_validation.validate_password(
            self.cleaned_data.get('password2'), self.instance)
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CreateProfileForm_user(forms.ModelForm):
    """
    Currently not in use as user is never asked for name.
    """
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name']

class CreateProfileForm_profile(forms.ModelForm):
    """
    Displayed during registration process.
    """
    #this override is neccessary to make sure that ----- is not displayed
    #for empty option; blank=True on the model is required for admin to allow
    #for empty field if sex is unknown
    sex = forms.TypedChoiceField(label='Płeć', choices=(
        ('K', 'Kobieta'),('M', 'Mężczyzna')), widget=forms.RadioSelect())
    
    class Meta:
        model = Profile
        fields = ['sex', 'career_start_year', 'education']

        widgets = {
            'sex': forms.RadioSelect()
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sex'].required = False

        
class PasswordResetCustomForm(PasswordResetForm):
    """
    Override to allow users with unusable passwords (authorized by social-oauth)
    to setup passwords.
    """
    
    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

            This allows subclasses to more easily customize the default policies
            that prevent inactive users [and users with unusable passwords - not any more] 
            from resetting their password.
            """
        UserModel = get_user_model()
        active_users = UserModel._default_manager.filter(**{
            '%s__iexact' % UserModel.get_email_field_name(): email,
            'is_active': True,
        })
        return (u for u in active_users)

class ActivationEmailSendAgainForm(forms.Form):
    """
    Input address where activation email should be resent.
    """
    email = forms.EmailField()

    
class ProfileUpdateForm(forms.ModelForm):
    """
    Display user profile form for modifications.
    """
    class Meta:
        model = Profile
        fields = '__all__'
        
    
