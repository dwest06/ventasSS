# Generated by Django 2.2.4 on 2019-08-11 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0003_auto_20190807_1924'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductoPedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('precio', models.FloatField(default=0)),
                ('descripcion', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='VentaStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_compra', models.PositiveIntegerField(default=0)),
                ('producto', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ventas.Stock')),
            ],
        ),
        migrations.AlterField(
            model_name='caja',
            name='cambio_dolar',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='producto',
            name='clase',
            field=models.CharField(choices=[('Eq', 'Equipo'), ('Es', 'Esencia'), ('R', 'Accesorios')], max_length=50),
        ),
        migrations.AlterField(
            model_name='venta',
            name='productos',
            field=models.ManyToManyField(to='ventas.VentaStock'),
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField()),
                ('imagen', models.ImageField(blank=True, upload_to='pedidos/')),
                ('descripcion', models.CharField(max_length=200)),
                ('total', models.FloatField(default=0)),
                ('productos', models.ManyToManyField(to='ventas.ProductoPedido')),
            ],
        ),
    ]
