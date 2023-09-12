from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import AppUser


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

    class Meta:
        model = AppUser
        fields = ('email', 'username', 'password1', 'password2', )
