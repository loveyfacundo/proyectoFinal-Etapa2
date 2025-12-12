# users/forms.py
from django import forms
from django.contrib.auth.models import User

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Repetir contraseña")

    class Meta:
        model = User
        fields = ['username', 'email']

    # Validación para que las contraseñas coincidan
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return cleaned_data
