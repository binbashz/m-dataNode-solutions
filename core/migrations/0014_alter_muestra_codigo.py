# Generated by Django 5.0.6 on 2024-06-15 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_product_is_favorite_product_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='muestra',
            name='codigo',
            field=models.CharField(max_length=100),
        ),
    ]