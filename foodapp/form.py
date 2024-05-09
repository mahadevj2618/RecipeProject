from django import forms
from foodapp.models import *

class ProfileForm(forms.ModelForm):  
    class Meta:
        model = Profile
        fields = ['image', 'bio', 'date_of_birth', 'education']