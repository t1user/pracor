from django import forms
from django.forms import ModelForm
from users.models import Profile

from django.contrib.auth import get_user_model

class CreateProfileForm_user(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name']

class CreateProfileForm_profile(forms.ModelForm):
    #this override is neccessary to make sure that ----- is not displayed
    #for empty option; blank=True on the model is required for admin to allow
    #for empty field if sex is unknown
    sex = forms.TypedChoiceField(label='Płeć', choices=(
        ('K', 'Kobieta'),('M', 'Mężczyzna')), widget=forms.RadioSelect())
    
    class Meta:
        model = Profile
        fields = ['sex', 'career_start_year']

        widgets = {
            'sex': forms.RadioSelect()
            }
        

