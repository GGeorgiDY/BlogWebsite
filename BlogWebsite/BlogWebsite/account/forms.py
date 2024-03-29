from django import forms
from django.contrib.auth.forms import UserCreationForm
# for authenticating users and if their credentials are valid
from django.contrib.auth import authenticate

from .models import AppUser


# here I used the pre-build UserCreationForm
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

    class Meta:
        model = AppUser
        fields = ('email', 'username', 'password1', 'password2', )


# here I will build custom form
class AccountAuthenticationForm(forms.ModelForm):
    # telling that the password field is type PasswordInput will make the password not visible
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = AppUser
        # telling which fields we will need
        fields = ('email', 'password')

    # this function is available to any form that extends the ModelForm. Before the form can do anything it has to run
    # this clean method. Any logic that is in this method will be executed before the form can actually do anything.
    # I do it this way because I want to be sure that the users credentials are valid and I will try to authenticate
    # them. If they are not valid I will provide some feedback.
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ('email', 'username', )

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        # check if this account exist and if it does not exist return the email and update the account with this email
        try:
            account = AppUser.objects.exclude(pk=self.instance.pk).get(email=email)
        except AppUser.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % email)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = AppUser.objects.exclude(pk=self.instance.pk).get(username=username)
        except AppUser.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)
