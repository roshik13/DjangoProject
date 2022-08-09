from pyexpat import model
from django.forms import ModelForm, fields
from django import forms
from .models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model=Profile
        fields=['name', 'email', 'college', 'major', 'year']