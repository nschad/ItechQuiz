from django.contrib.auth.forms import AuthenticationForm
from django import forms


class BootstrapAuthenticationForm(AuthenticationForm):
    # id="inputEmail" class="form-control" placeholder="Email address" required="" autofocus=""
    username = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'inputUsername', 'placeholder': 'Username', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'id': 'inputPassword', 'type': 'password', 'placeholder': 'Password', 'class': 'form-control'}))

