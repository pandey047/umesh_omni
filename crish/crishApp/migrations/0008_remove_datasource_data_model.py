# Generated by Django 4.0.3 on 2022-06-15 05:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crishApp', '0007_datasource_data_model_alter_datasource_sql_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datasource',
            name='data_model',
        ),
    ]
