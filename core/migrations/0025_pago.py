# Generated by Django 5.0.6 on 2024-07-04 03:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_cannabisplant'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('miembro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.miembro')),
            ],
        ),
    ]
