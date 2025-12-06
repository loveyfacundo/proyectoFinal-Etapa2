from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Perfil


# Crea automáticamente un Perfil cuando se crea un nuevo User
@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):

    if created:
        Perfil.objects.create(
            usuario=instance,
            # Rol predeterminado
            rol='miembro'
        )
        print(f"✓ Perfil creado automáticamente para {instance.username}")


# Guarda el perfil cuando se actualiza el usuario
@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    
    if hasattr(instance, 'perfil'):
        instance.perfil.save()
        print(f"✓ Perfil actualizado para {instance.username}")