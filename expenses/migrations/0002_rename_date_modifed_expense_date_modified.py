# Generated by Django 3.2.6 on 2021-08-25 10:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='date_modifed',
            new_name='date_modified',
        ),
    ]
