# Generated by Django 4.2.3 on 2023-08-30 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagos', '0008_pago_banco_destino_pago_cuenta_pago_fecha_deposito_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pago',
            name='administracion',
            field=models.CharField(blank=True, choices=[('1Pendiente', 'Pendiente'), ('2Aprobado', 'Aprobado'), ('3Rechazado', 'Rechazado')], default='1Pendiente', max_length=30),
        ),
        migrations.AddField(
            model_name='pago',
            name='carga_crm',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
