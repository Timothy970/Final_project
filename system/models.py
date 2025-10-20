from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator
import pycountry
from django.utils.translation import gettext_lazy as _
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django. template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
# Create your models here.
# class Donors(models.Model):
    
#     user = models.OneToOneField(settings.AUTH_USER_MODEL,
#                                  on_delete=models.CASCADE)
#     fname = models.CharField(max_length=30)
#     lname = models.CharField(max_length=30)
#     dob = models.DateField()
#     email = models.CharField(max_length=50)
#     photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
#     city = models.CharField(max_length=30)
#     blood_type = models.CharField(max_length=30)
#     availability = models.CharField(max_length=30)
    
#     def __str__(self):
#         return f'Donors of {self.user.username}'


gender_choices = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other')
    )
city_choices =(
    ('Baragoi', 'Baragoi'),
    ('Bondo', 'Bondo'),
    ('Bungoma', 'Bungoma'),
    ('Busia', 'Busia'),
    ('Butere', 'Butere'),
    ('Dadaab', 'Dadaab'),
    ('Diani Beach', 'Diani Beach'),
    ('Eldoret', 'Eldoret'),
    ('Emali', 'Emali'),
    ('Embu', 'Embu'),
    ('Garissa', 'Garissa'),
    ('Gede', 'Gede'),
    ('Hola', 'Hola'),
    ('Homa Bay', 'Homa Bay'),
    ('Isiolo', 'Isiolo'),
    ('Kitui', 'Kitui'),
    ('Kibwezi', 'Kibwezi'),
    ('Kajiado', 'Kajiado'),
    ('Kakamega', 'Kakamega'),
    ('Kakuma', 'Kakuma'),
    ('Kapenguria', 'Kapenguria'),
    ('Kericho', 'Kericho'),
    ('Kiambu', 'Kiambu'),
    ('Kilifi', 'kilifi'),
    ('Kisii', 'Kisii'),
    ('Kisumu', 'Kisumu'),
    ('Kitale', 'Kitale'),
    ('Lamu', 'Lamu'),
    ('Langata', 'Langata'),
    ('Litein', 'Litien'),
    ('Lodwar', 'Lodwar'),
    ('Lokichoggio', 'Lokichoggio'),
    ('Londiani', 'Londiani'),
    ('Machakos', 'Machakos'),
    ('Malindi', 'Malindi'),
    ('Mandera', 'Mandera'),
    ('Maralal', 'Maralal'),
    ('Marsabit', 'Marsabit'),
    ('Meru', 'Meru'),
    ('Mombasa', 'Mombasa'),
    ('Moyale', 'Moyale'),
    ('Mtwapa', 'Mtwapa'),
    ('Mumias', 'Mumias'),
    ('Muranga', 'Muranga'),
    ('Nairobi', 'Nairobi'),
    ('Naivasha', 'Naivasha'),
    ('Nakuru', 'Nakuru'),
    ('Namanga', 'Namanga'),
    ('Nanyuki', 'Nanyuki'),
    ('Naro Moru', 'Naro Moru'),
    ('Narok', 'Narok'),
    ('Nyahururu', 'Nyahururu'),
    ('Nyeri', 'Nyeri'),
    ('Ruiru', 'Ruiru'),
    ('Siaya', 'Siaya'),
    ('Thika', 'Thika'),
    ('Ugunja', 'Ugunja'),
    ('Vihiga', 'Vihiga'),
    ('Voi', 'Voi'),
    ('Wajir', 'Wajir'),
    ('Watamu', 'Watamu'),
    ('Webuye', 'Webuye'),
    ('Wote', 'Wote'),
    ('Wundanyi', 'Wundanyi')
    )
availability_choices=(
    ('Anyday', 'Any Day'),
    ('Weekdays', 'Week Days'),
    ('Weekends', 'Weekends')
    )
bloodtype_choices=(
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('B+', 'B+'),
    ('A-', 'A-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
)
def validate_age(value):
    today = date.today()
    age_limit = today - timedelta(days=16 * 365)
    if value > age_limit:
        raise ValidationError(
            _('You must be 16 years or older'),
            params={'value': value},
        )
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # id = models.AutoField(primary_key=True)
    date_of_birth = models.DateField(null=True, validators=[validate_age])
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    availability = models.CharField(max_length=200, choices=availability_choices, default='Anyday')
    gender = models.CharField(
    max_length=100,
    choices=gender_choices,
    null=True,
    blank=True
)
    blood_type = models.CharField(max_length=100,choices=bloodtype_choices, default='A+')
    city = models.CharField(max_length=100,choices=city_choices, default='Nairobi')

    phone_number = PhoneNumberField()

    def get_whatsapp_link(self):
        if self.phone_number:
            whatsapp_number = f"{self.phone_number}"
            return f"https://wa.me/{whatsapp_number}?text=Hello%20Blood%20Heroe"
        return None

    
    def __str__(self):
        return f'Profile of {self.user.username}'
    
    
class DonationSchedule(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    time_slot = models.TimeField() 
    
    
class BloodDonationBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"Blood Donation Booking for {self.first_name} {self.last_name}"
    


class BloodRequest(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    blood_type = models.CharField(max_length=10,choices=bloodtype_choices)
    contact_number = PhoneNumberField()
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

                                                                 
                              
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blood_request = models.ForeignKey(BloodRequest, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Donation_Made(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100)
    blood_type = models.CharField(max_length=10, choices=bloodtype_choices)
    quantity = models.PositiveIntegerField()
    notes = models.TextField(blank= True, null=True)
    points_earned = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.donor.username}'s donation on {self.date} at {self.time}."
    

class Chat(models.Model):
    participants = models.ManyToManyField(User)
    created_at = models.DateTimeField(default=timezone.now)

class Message(models.Model):
    chat = models.ForeignKey(
        Chat,
        related_name='messages',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_message')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recieved_message')
    content = models.TextField()
    is_read = models.BooleanField(default=False) 
    timestamp = models.DateTimeField(default=timezone.now)   

    class Meta:
        ordering = ['timestamp']