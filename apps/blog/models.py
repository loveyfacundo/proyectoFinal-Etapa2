from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Perfil(models.Model):
    USUARIO_ROLES = [
        ('miembro', 'Miembro'),
        ('colaborador', 'Colaborador'),
        # El admin es el superuser de Django
    ]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=USUARIO_ROLES, default='miembro')

    def __str__(self):
        return f"{self.usuario.username} - {self.get_rol_display()}"


class Articulo(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='articulos')
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='articulos')
    imagen_destacada = models.ImageField(upload_to='articulos/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    destacado = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comentarios')
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comentario de {self.autor} en {self.articulo.titulo}'


class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=120)
    email = models.EmailField()
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    gestionado = models.BooleanField(default=False)

    def __str__(self):
        return f"Mensaje de {self.nombre} ({self.email})"


class AcercaDe(models.Model):
    contenido = models.TextField()
    integrantes = models.TextField(blank=True, null=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)