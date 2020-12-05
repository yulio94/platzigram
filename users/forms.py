"""User forms."""

# Django
from django import forms

# Models
from django.contrib.auth.models import User
import users.models as models


class SignupForm(forms.Form):
    """Sign up form."""
    username = forms.CharField(min_length=4, max_length=50)
    first_name = forms.CharField(min_length=2, max_length=50)
    last_name = forms.CharField(min_length=2, max_length=50)
    email = forms.CharField(min_length=6, max_length=70, widget=forms.EmailInput())
    password = forms.CharField(max_length=70, widget=forms.PasswordInput())
    password_confirmation = forms.CharField(max_length=70, widget=forms.PasswordInput())

    def clean_username(self):
        """Username must be unique."""
        username = self.cleaned_data['username']
        username_taken = User.objects.filter(username=username).exists()

        if username_taken:
            raise forms.ValidationError('Username is already in use.')

        return username

    def clean(self):
        """Verify password confirmation match."""
        data = super().clean()

        password = data['password']
        password_confirmation = data['password_confirmation']

        if password_confirmation != password:
            raise forms.ValidationError('Password don\'t match')

        return data

    def save(self):
        data = self.cleaned_data
        data.pop('password_confirmation')

        user = User.objects.create_user(**data)
        profile = models.Profile(user=user)
        profile.save()
