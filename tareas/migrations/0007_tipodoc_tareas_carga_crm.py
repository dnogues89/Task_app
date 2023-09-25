# Generated by Django 4.2.3 on 2023-09-20 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tareas', '0006_preventa_fecha_preventa_preventa_modelo'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoDoc',
            fields=[
                ('tipo_id', models.IntegerField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='tareas',
            name='carga_crm',
            field=models.BooleanField(default=False),
        ),
    ]
