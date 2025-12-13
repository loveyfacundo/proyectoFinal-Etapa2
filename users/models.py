from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Perfil(models.Model):
    ROL_CHOICES = [
        ('miembro', 'Miembro'),
        ('colaborador', 'Colaborador'),
        ('administrador', 'Administrador'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_users')
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='miembro')

    def __str__(self):
        return f'{self.user.username} - {self.rol}'


@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)


@receiver(post_save, sender=User)
def guardar_perfil(sender, instance, **kwargs):
    # FIX 🟢 Evita error cuando el user aún no tiene perfil
    if hasattr(instance, 'perfil_users'):
        instance.perfil_users.save()

