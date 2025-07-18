# Generated by Django 5.2.3 on 2025-07-13 18:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizacao', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plano',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('nome', models.CharField(max_length=100)),
                ('data_nascimento', models.DateField(blank=True, null=True)),
                ('sexo', models.CharField(blank=True, choices=[('M', 'Masculino'), ('F', 'Feminino')], max_length=1, null=True)),
                ('telefone', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('plano_status', models.BooleanField(default=True)),
                ('data_inicio', models.DateField(blank=True, null=True)),
                ('data_fim', models.DateField(blank=True, null=True)),
                ('condicoes_medicas', models.CharField(blank=True, max_length=255, null=True)),
                ('ciclo_menstrual', models.CharField(blank=True, max_length=100, null=True)),
                ('medicamentos', models.CharField(blank=True, max_length=255, null=True)),
                ('lesoes', models.CharField(blank=True, max_length=255, null=True)),
                ('ocupacao', models.CharField(blank=True, max_length=100, null=True)),
                ('estilo_vida', models.CharField(blank=True, max_length=100, null=True)),
                ('pratica_esportes', models.CharField(blank=True, max_length=100, null=True)),
                ('pratica_exercicios', models.CharField(blank=True, max_length=100, null=True)),
                ('dias_disponiveis', models.CharField(blank=True, max_length=100, null=True)),
                ('horario_preferencia', models.CharField(blank=True, max_length=100, null=True)),
                ('exercicio_preferencia', models.CharField(blank=True, max_length=100, null=True)),
                ('info_adicional', models.CharField(blank=True, max_length=255, null=True)),
                ('tempo_atual_treino', models.CharField(blank=True, max_length=100, null=True)),
                ('tempo_destreinado', models.CharField(blank=True, max_length=100, null=True)),
                ('tempo_treino_anterior', models.CharField(blank=True, max_length=100, null=True)),
                ('organizacao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organizacao.organizacao')),
                ('plano_tipo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='alunos.plano')),
            ],
            options={
                'verbose_name': 'Aluno',
                'verbose_name_plural': 'Alunos',
                'ordering': ['nome'],
            },
        ),
    ]
