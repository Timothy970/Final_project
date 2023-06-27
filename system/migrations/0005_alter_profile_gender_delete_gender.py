# Generated by Django 4.2.1 on 2023-06-21 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0004_alter_profile_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='Male', max_length=100),
        ),
        migrations.DeleteModel(
            name='gender',
        ),
    ]