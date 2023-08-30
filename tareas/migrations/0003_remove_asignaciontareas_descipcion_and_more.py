# Generated by Django 4.2.3 on 2023-08-28 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tareas', '0002_tipotarea_asignaciontareas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asignaciontareas',
            name='descipcion',
        ),
        migrations.AddField(
            model_name='asignaciontareas',
            name='descripcion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='asignaciontareas',
            name='descarga',
            field=models.FileField(blank=True, null=True, upload_to='archivos_para_descargar'),
        ),
    ]