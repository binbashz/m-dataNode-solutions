# Generated by Django 5.0.6 on 2024-06-10 04:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_analisiscostos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=200)),
                ('telefono', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='TipoAnalisis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('metodo', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TipoMuestra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Muestra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=20, unique=True)),
                ('fecha_recepcion', models.DateField()),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.cliente')),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.tipomuestra')),
            ],
        ),
        migrations.CreateModel(
            name='AnalisisProgramado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_programada', models.DateTimeField()),
                ('prioridad', models.IntegerField(choices=[(1, 'Baja'), (2, 'Media'), (3, 'Alta')])),
                ('muestra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.muestra')),
                ('tipo_analisis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.tipoanalisis')),
            ],
        ),
        migrations.CreateModel(
            name='ResultadoAnalisis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_analisis', models.DateTimeField()),
                ('resultados', models.JSONField()),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('analisis_programado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.analisisprogramado')),
            ],
        ),
    ]
