from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User

from .models import Comentario, Articulo, MensajeContacto

class RegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Escribe tu comentario aquí...',
                'style': 'width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ccc;'
            }),
        }

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ['titulo', 'contenido', 'categoria', 'imagen_destacada', 'destacado']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título del artículo'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }

class ContactoForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tu@email.com'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Escribe tu mensaje...'}),
        }

class EditarPerfilForm(forms.ModelForm):
    """Formulario para editar datos básicos del usuario"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa tu nombre'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa tu apellido'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'tu@email.com'
            }),
        }

class CambiarPasswordForm(PasswordChangeForm):
    """Formulario personalizado para cambiar contraseña"""
    old_password = forms.CharField(
        label='Contraseña Actual',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '••••••••'
        })
    )
    new_password1 = forms.CharField(
        label='Nueva Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '••••••••'
        })
    )
    new_password2 = forms.CharField(
        label='Confirmar Nueva Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '••••••••'
        })
    )