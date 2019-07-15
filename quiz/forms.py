from django.contrib.auth.forms import AuthenticationForm
from django import forms


class BootstrapAuthenticationForm(AuthenticationForm):
    # id="inputEmail" class="form-control" placeholder="Email address" required="" autofocus=""
    username = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'inputUsername', 'placeholder': 'Username', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'id': 'inputPassword', 'type': 'password', 'placeholder': 'Password', 'class': 'form-control'}))


class MySuperCustomCheckboxField(forms.CheckboxInput):

    def __init__(self, question_name=""):
        super().__init__()
        self.question_name = question_name


class PlayForm(forms.Form):
    def __init__(self, formdata: dict = None):
        super().__init__()

        if formdata is None:
            raise ValueError("Passing no form data is kinda Shitty mate.")

        questions = formdata["options"]

        for question in questions:
            original_question_text = question
            question_id = question.replace(" ", "_").strip()
            self.fields[question_id] = forms.CharField(widget=MySuperCustomCheckboxField(
                question_name=original_question_text))


