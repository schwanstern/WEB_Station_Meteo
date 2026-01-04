from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    identifiant = forms.CharField(
        label="Utilisateur / Email",
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg rounded-3 fs-6'}),
        required=True
    )
    mdp = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg rounded-start-3 fs-6', 'id': 'passwordInput'}),
        required=True
    )


class RegisterForm(forms.Form):
    identifiant = forms.CharField(
        label="Utilisateur",
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg rounded-3 fs-6'}),
        required=True
    )
    email = forms.EmailField(
        label="Adresse Email",
        widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg rounded-3 fs-6'}),
        required=True
    )
    mdp = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg rounded-start-3 fs-6'}),
        required=True
    )

    def clean_identifiant(self):
        username = self.cleaned_data['identifiant']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Ce nom d'utilisateur est déjà pris.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Cet email est déjà utilisé.")
        return email


class UpdateSystemForm(forms.Form):
    do_update = forms.CharField(widget=forms.HiddenInput(), initial="true")
