# Generated by Django 4.2.3 on 2023-10-05 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tareas', '0016_tareas_crm_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='preventa',
            name='tareas_de_usuario_crm',
            field=models.BooleanField(default=False),
        ),
    ]
