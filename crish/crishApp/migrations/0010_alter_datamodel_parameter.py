# Generated by Django 4.0.3 on 2022-06-16 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crishApp', '0009_alter_databaseconnection_parameter_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datamodel',
            name='parameter',
            field=models.FileField(blank=True, null=True, upload_to='uploads/datamodels'),
        ),
    ]
