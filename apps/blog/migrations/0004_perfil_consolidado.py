# Generated manually to consolidate Perfil model from users app to blog app

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_perfil_rol'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Esta migración asume que la tabla blog_perfil ya existe con los datos de users_perfil
        # Actualiza el related_name de perfil_users a perfil
        migrations.AlterField(
            model_name='perfil',
            name='user',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='perfil',
                to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
