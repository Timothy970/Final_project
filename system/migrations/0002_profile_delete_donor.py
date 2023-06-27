# Generated by Django 4.2.1 on 2023-06-21 12:22

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
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, upload_to='users/%Y/%m/%d/')),
                ('availability', models.CharField(choices=[('Anyday', 'Any Day'), ('Weekdays', 'Week Days'), ('Weekends', 'Weekends')], max_length=200)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=100)),
                ('blood_type', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('A-', 'A-'), ('O+', 'O+'), ('O-', 'O-')], max_length=100)),
                ('city', models.CharField(choices=[('Baragoi', 'Baragoi'), ('Bondo', 'Bondo'), ('Bungoma', 'Bungoma'), ('Busia', 'Busia'), ('Butere', 'Butere'), ('Dadaab', 'Dadaab'), ('Diani Beach', 'Diani Beach'), ('Eldoret', 'Eldoret'), ('Emali', 'Emali'), ('Embu', 'Embu'), ('Garissa', 'Garissa'), ('Gede', 'Gede'), ('Hola', 'Hola'), ('Homa Bay', 'Homa Bay'), ('Isiolo', 'Isiolo'), ('Kitui', 'Kitui'), ('Kibwezi', 'Kibwezi'), ('Kajiado', 'Kajiado'), ('Kakamega', 'Kakamega'), ('Kakuma', 'Kakuma'), ('Kapenguria', 'Kapenguria'), ('Kericho', 'Kericho'), ('Kiambu', 'Kiambu'), ('Kilifi', 'kilifi'), ('Kisii', 'Kisii'), ('Kisumu', 'Kisumu'), ('Kitale', 'Kitale'), ('Lamu', 'Lamu'), ('Langata', 'Langata'), ('Litein', 'Litien'), ('Lodwar', 'Lodwar'), ('Lokichoggio', 'Lokichoggio'), ('Londiani', 'Londiani'), ('Machakos', 'Machakos'), ('Malindi', 'Malindi'), ('Mandera', 'Mandera'), ('Maralal', 'Maralal'), ('Marsabit', 'Marsabit'), ('Meru', 'Meru'), ('Mombasa', 'Mombasa'), ('Moyale', 'Moyale'), ('Mtwapa', 'Mtwapa'), ('Mumias', 'Mumias'), ('Muranga', 'Muranga'), ('Nairobi', 'Nairobi'), ('Naivasha', 'Naivasha'), ('Nakuru', 'Nakuru'), ('Namanga', 'Namanga'), ('Nanyuki', 'Nanyuki'), ('Naro Moru', 'Naro Moru'), ('Narok', 'Narok'), ('Nyahururu', 'Nyahururu'), ('Nyeri', 'Nyeri'), ('Ruiru', 'Ruiru'), ('Siaya', 'Siaya'), ('Thika', 'Thika'), ('Ugunja', 'Ugunja'), ('Vihiga', 'Vihiga'), ('Voi', 'Voi'), ('Wajir', 'Wajir'), ('Watamu', 'Watamu'), ('Webuye', 'Webuye'), ('Wote', 'Wote'), ('Wundanyi', 'Wundanyi')], max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Donor',
        ),
    ]
