from django import forms
from django.core.exceptions import ValidationError
import re

class CustomAuthenticationForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get("username")
        # Verifica que el correo tenga un dominio válido
        if not (username.endswith('@gmail.com') or username.endswith('@hotmail.com')):
            raise ValidationError("El correo electrónico debe ser de tipo @gmail.com o @hotmail.com.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get("password")
        # Verifica que la contraseña tenga al menos una letra mayúscula
        if not any(char.isupper() for char in password):
            raise ValidationError("La contraseña debe tener al menos una letra mayúscula.")
        return password