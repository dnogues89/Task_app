# Generated by Django 4.2.3 on 2023-08-24 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagos', '0005_alter_pago_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='pago',
            name='depositante_cuit',
            field=models.IntegerField(default=1, verbose_name='Datos Depositante'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pago',
            name='estado',
            field=models.CharField(blank=True, choices=[('1Pendiente', 'Pendiente'), ('2Aprobado', 'Aprobado'), ('3Rechazado', 'Rechazado')], default='1Pendiente', max_length=30),
        ),
    ]