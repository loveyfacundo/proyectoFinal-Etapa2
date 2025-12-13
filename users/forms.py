from django import forms
from django.contrib.auth.models import User
from .models import Perfil

# --- FORMULARIO DE REGISTRO ---
class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Repetir contraseña")

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

# --- FORMULARIO DE EDICIÓN DE PERFIL ---
class PerfilForm(forms.ModelForm):
    email = forms.EmailField(label="Correo electrónico")

    class Meta:
        model = Perfil
        fields = ['avatar', 'bio']  # Cambia estos campos según tu modelo

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        perfil = super().save(commit=False)
        if 'email' in self.cleaned_data:
            perfil.user.email = self.cleaned_data['email']
            perfil.user.save()
        if commit:
            perfil.save()
        return perfil
