# Generated by Django 5.0.6 on 2024-07-08 19:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_venta_variedad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gastooperativo',
            name='variedad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.variedad'),
        ),
    ]