# Generated by Django 4.2.3 on 2023-11-09 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConvertPDF',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo1', models.ImageField(upload_to='temp')),
                ('archivo2', models.ImageField(upload_to='temp')),
                ('archivo3', models.ImageField(upload_to='temp')),
                ('archivo4', models.ImageField(upload_to='temp')),
                ('archivo5', models.ImageField(upload_to='temp')),
                ('archivo6', models.ImageField(upload_to='temp')),
                ('pdf', models.FileField(upload_to='pdf')),
            ],
        ),
    ]
