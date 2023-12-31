# Generated by Django 4.2.6 on 2023-11-26 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0017_carrito_estado'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaypalPago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=250)),
                ('contraseña', models.CharField(max_length=250)),
                ('total_carrito', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('id_carrito', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='venta.carrito')),
            ],
            options={
                'verbose_name_plural': 'Pagos_de_Paypal',
            },
        ),
        migrations.DeleteModel(
            name='Pedido',
        ),
    ]
