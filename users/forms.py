from django import forms
from django.forms import ModelForm
from users.models import Profile

from django.contrib.auth import get_user_model

class CreateProfileForm_user(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name']

class CreateProfileForm_profile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['sex', 'career_start_year']

        widgets = {
            'sex': forms.RadioSelect()
            }
        
