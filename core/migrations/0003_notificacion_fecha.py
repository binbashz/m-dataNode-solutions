# Generated by Django 5.0.7 on 2024-07-11 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_notificacion_pedido'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificacion',
            name='fecha',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
