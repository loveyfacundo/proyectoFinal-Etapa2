from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import (
    Categoria, Perfil, Articulo, Comentario, MensajeContacto, AcercaDe
)

# Register your models here.

# Inline para mostrar el Perfil dentro del User
class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil'
    fields = ['rol']

# Extender el UserAdmin para incluir el Perfil
class UserAdmin(BaseUserAdmin):
    inlines = [PerfilInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'get_rol', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'perfil__rol']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    
    def get_rol(self, obj):
        """Obtiene el rol del usuario desde su perfil"""
        try:
            return obj.perfil.get_rol_display()
        except Perfil.DoesNotExist:
            return 'Sin perfil'
    get_rol.short_description = 'Rol'

# Re-registrar UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'rol', 'get_email']
    list_filter = ['rol']
    search_fields = ['usuario__username', 'usuario__email']
    
    def get_email(self, obj):
        """Muestra el email del usuario"""
        return obj.usuario.email
    get_email.short_description = 'Email'

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