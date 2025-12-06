from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Comentario, Articulo

class RegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        # Django se encarga de las contraseñas automáticamente con UserCreationForm

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

