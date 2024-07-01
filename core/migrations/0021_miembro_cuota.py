# Generated by Django 5.0.6 on 2024-06-30 18:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_listamateriales_material_planproduccion_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Miembro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_socio', models.CharField(max_length=10, unique=True)),
                ('fecha_ingreso', models.DateField()),
                ('activo', models.BooleanField(default=True)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cuota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_pago', models.DateField()),
                ('monto', models.DecimalField(decimal_places=2, max_digits=8)),
                ('periodo', models.CharField(choices=[('MENSUAL', 'Mensual'), ('TRIMESTRAL', 'Trimestral'), ('ANUAL', 'Anual')], max_length=10)),
                ('pagado', models.BooleanField(default=False)),
                ('miembro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.miembro')),
            ],
        ),
    ]
