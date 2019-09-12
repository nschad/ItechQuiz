from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation


class BootstrapAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'inputUsername', 'placeholder': 'Username', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'id': 'inputPassword', 'type': 'password', 'placeholder': 'Password', 'class': 'form-control'}))


class BootsrapRegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'id': 'password1', 'type': 'password', 'placeholder': 'Password', 'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'id': 'password2', 'type': 'password', 'placeholder': 'Password', 'class': 'form-control'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

