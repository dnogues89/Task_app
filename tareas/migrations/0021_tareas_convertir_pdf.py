# Generated by Django 4.2.3 on 2023-11-09 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pdfs', '0002_alter_convertpdf_archivo2_alter_convertpdf_archivo3_and_more'),
        ('tareas', '0020_alter_preventa_tareas_de_usuario_crm'),
    ]

    operations = [
        migrations.AddField(
            model_name='tareas',
            name='convertir_pdf',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pdfs.convertpdf'),
        ),
    ]