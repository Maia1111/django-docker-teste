# Generated by Django 5.0.6 on 2024-06-08 16:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0008_alter_usuario_matricula_alter_usuario_numero'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='usuario_validador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='validador', to=settings.AUTH_USER_MODEL),
        ),
    ]
