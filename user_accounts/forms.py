from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User



class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')


class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone')
