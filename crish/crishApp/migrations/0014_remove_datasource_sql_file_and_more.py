# Generated by Django 4.0.3 on 2022-07-20 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crishApp', '0013_alter_datamodel_creationuser_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datasource',
            name='sql_file',
        ),
        migrations.AlterField(
            model_name='databaseconnection',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='datamodel',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='datasource',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='explorer',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]