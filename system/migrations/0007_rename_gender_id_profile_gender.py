# Generated by Django 4.2.1 on 2023-06-21 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0006_rename_gender_profile_gender_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='gender_id',
            new_name='gender',
        ),
    ]
