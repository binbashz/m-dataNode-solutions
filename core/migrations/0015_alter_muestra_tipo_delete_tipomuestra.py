# Generated by Django 5.0.6 on 2024-06-16 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_muestra_codigo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='muestra',
            name='tipo',
            field=models.CharField(max_length=100),
        ),
        migrations.DeleteModel(
            name='TipoMuestra',
        ),
    ]