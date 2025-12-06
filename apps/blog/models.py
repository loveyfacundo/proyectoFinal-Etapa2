from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Perfil(models.Model):
    USUARIO_ROLES = [
        ('miembro', 'Miembro'),
        ('colaborador', 'Colaborador'),
        ('administrador', 'Administrador'),
    ]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=USUARIO_ROLES, default='miembro')

    class Meta:
        verbose_name_plural = "Perfiles"

    def __str__(self):
        return f"{self.usuario.username} - {self.get_rol_display()}"
    
    def es_administrador(self):
        """Verifica si el usuario tiene rol de administrador"""
        return self.rol == 'administrador'
    
    def es_colaborador_o_superior(self):
        """Verifica si el usuario es colaborador o administrador"""
        return self.rol in ['colaborador', 'administrador']
    
    def puede_gestionar_usuarios(self):
        """Solo administradores pueden gestionar usuarios"""
        return self.rol == 'administrador'


class Articulo(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='articulos')
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='articulos')
    imagen_destacada = models.ImageField(upload_to='articulos/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    destacado = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Artículos"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comentarios')
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Comentarios"
        ordering = ['fecha_creacion']

    def __str__(self):
        return f'Comentario de {self.autor} en {self.articulo.titulo}'


class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=120)
    email = models.EmailField()
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    gestionado = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Mensajes de Contacto"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Mensaje de {self.nombre} ({self.email})"


class AcercaDe(models.Model):
    contenido = models.TextField()
    integrantes = models.TextField(blank=True, null=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Acerca de"
        verbose_name_plural = "Acerca de"

    def __str__(self):
        return f"Acerca de (actualizado: {self.fecha_actualizacion.strftime('%d/%m/%Y')})"