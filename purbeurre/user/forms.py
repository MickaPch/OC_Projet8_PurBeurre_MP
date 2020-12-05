"""User forms"""
from django import forms
from django.contrib.auth.validators import UnicodeUsernameValidator

class ConnectionForm(forms.Form):
    """Connection form"""
    user_login = forms.CharField(label="Email ou login")
    pwd = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

    user_login.widget.attrs.update(
        {
            'class': 'form-control',
            'placeholder': 'Email ou login'
        }
    )
    pwd.widget.attrs.update(
        {
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        }
    )

class NewForm(forms.Form):
    """New account form"""

    username_validator = UnicodeUsernameValidator()

    email = forms.EmailField(label="Email *")
    user_login = forms.CharField(
        max_length=150,
        validators=[username_validator],
        required=False
    )
    pwd = forms.CharField(
        label="Mot de passe *",
        widget=forms.PasswordInput
    )
    pwd_confirm = forms.CharField(
        label="Confirmation du mot de passe",
        widget=forms.PasswordInput
    )
    firstname = forms.CharField(
        label="Prénom",
        max_length=30,
        required=False,
    )
    lastname = forms.CharField(
        label="Nom",
        max_length=30,
        required=False,
    )

    email.widget.attrs.update(
        {
            'class': 'form-control is-invalid',
            'placeholder': 'Email'
        }
    )
    user_login.widget.attrs.update(
        {
            'class': 'form-control',
            'placeholder': 'Login'
        }
    )
    pwd.widget.attrs.update(
        {
            'class': 'form-control is-invalid',
            'placeholder': 'Mot de passe'
        }
    )
    pwd_confirm.widget.attrs.update(
        {
            'class': 'form-control is-invalid',
            'placeholder': 'Veuillez retaper le mot de passe'
        }
    )
    firstname.widget.attrs.update(
        {
            'class': 'form-control',
            'placeholder': 'Prénom'
        }
    )
    lastname.widget.attrs.update(
        {
            'class': 'form-control',
            'placeholder': 'Nom'
        }
    )

    def clean(self):
        cleaned_data = super(NewForm, self).clean()
        pwd = cleaned_data.get("pwd")
        pwd_confirm = cleaned_data.get("pwd_confirm")

        if pwd != pwd_confirm:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )