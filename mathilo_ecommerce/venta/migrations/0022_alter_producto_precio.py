# Generated by Django 4.2.6 on 2023-11-29 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0021_alter_producto_precio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='precio',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]
