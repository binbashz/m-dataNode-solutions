from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='variedad',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='productos',
                to='core.variedad',
                null=True  # Add this if you have existing products
            ),
        ),
    ]