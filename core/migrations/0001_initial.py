# Generated by Django 5.2.3 on 2025-07-13 18:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizacao', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PerfilUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpf', models.CharField(blank=True, max_length=14, null=True, unique=True)),
                ('nivel_acesso', models.CharField(choices=[('usuario', 'Usuário'), ('admin', 'Administrador'), ('master', 'Master')], default='usuario', max_length=10)),
                ('status_bloqueio', models.BooleanField(default=False)),
                ('primeiro_acesso', models.BooleanField(default=True)),
                ('organizacao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organizacao.organizacao')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Perfil de Usuário',
                'verbose_name_plural': 'Perfis de Usuários',
            },
        ),
    ]
