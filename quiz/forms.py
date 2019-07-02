from django.contrib.auth.forms import AuthenticationForm
from django import forms


class BootstrapAuthenticationForm(AuthenticationForm):
    # id="inputEmail" class="form-control" placeholder="Email address" required="" autofocus=""
    username = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'inputUsername', 'placeholder': 'Username', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'id': 'inputPassword', 'type': 'password', 'placeholder': 'Password', 'class': 'form-control'}))


class PlayForm(forms.Form):
    def __init__(self, formdata: dict = None):
        super().__init__()

        if formdata is None:
            raise ValueError("Passing no farmdata is kinda Shitty mate.")

        for id, question in formdata:
            self.fields[id] = forms.CharField(widget=forms.CheckboxInput(attrs={'type': 'checkbox', 'class': 'filled-in'}))
