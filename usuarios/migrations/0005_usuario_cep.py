# Generated by Django 5.0.6 on 2024-06-02 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_rename_mudança_senha_usuario_mudanca_senha'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='cep',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
