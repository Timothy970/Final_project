# Generated by Django 4.2.1 on 2023-06-06 08:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donor1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=30)),
                ('lname', models.CharField(max_length=30)),
                ('dob', models.DateField()),
                ('email', models.CharField(max_length=50)),
                ('phone_no', models.IntegerField()),
                ('city', models.CharField(max_length=30)),
                ('blood_type', models.CharField(max_length=30)),
                ('availability', models.CharField(max_length=30)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Donor',
        ),
    ]
