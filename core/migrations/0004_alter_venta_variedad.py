# Generated by Django 5.0.6 on 2024-07-08 18:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_product_variedad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venta',
            name='variedad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.variedad'),
        ),
    ]