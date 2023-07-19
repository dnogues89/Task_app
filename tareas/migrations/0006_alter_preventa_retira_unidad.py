# Generated by Django 4.2.3 on 2023-07-19 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tareas', '0005_preventa_completo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preventa',
            name='retira_unidad',
            field=models.CharField(blank=True, choices=[(1, 'Transportista'), (2, 'Individuo'), (3, 'Titular')], max_length=15, null=True),
        ),
    ]
