from django.contrib import admin
from .models import (
    Categoria, Perfil, Articulo, Comentario, MensajeContacto, AcercaDe
)

# Register your models here.
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'rol']
    search_fields = ['usuario__username', 'rol']

@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'categoria', 'destacado', 'fecha_creacion']
    list_filter = ['categoria', 'destacado', 'fecha_creacion']
    search_fields = ['titulo', 'contenido']

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['articulo', 'autor', 'fecha_creacion']
    search_fields = ['contenido', 'autor__username']

@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'fecha_creacion', 'gestionado']
    list_filter = ['gestionado']
    search_fields = ['nombre', 'email', 'mensaje']

@admin.register(AcercaDe)
class AcercaDeAdmin(admin.ModelAdmin):
    list_display = ['fecha_actualizacion']