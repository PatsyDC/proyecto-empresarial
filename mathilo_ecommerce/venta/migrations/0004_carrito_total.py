# Generated by Django 4.2.6 on 2023-11-02 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0003_carrito'),
    ]

    operations = [
        migrations.AddField(
            model_name='carrito',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
