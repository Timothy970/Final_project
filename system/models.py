from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    ('B+', 'B+'),
    ('A-', 'A-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # id = models.AutoField(primary_key=True)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    availability = models.CharField(max_length=200, choices=availability_choices, default='Anyday')
    gender = models.CharField(max_length=100, default='Male')
    blood_type = models.CharField(max_length=100, default='A+')
    city = models.CharField(max_length=100, default='Nairobi')
    phone_number = models.CharField(max_length=20, default='your number')
    
    
    def __str__(self):
        return f'Profile of {self.user.username}'
    
    
class DonationSchedule(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    time_slot = models.TimeField() 
    
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_message')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recieved_message')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)   
# @receiver(post_save, sender=User)    
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
    
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
    
    

   
# class Recipient(models.Model):

#     username = models.CharField(max_length=150, unique=True)
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     email = models.EmailField(unique=True)
#     # dob = models.DateField()
#     gender = models.CharField(max_length=1, choices=gender_choices)
    # user_type = models.CharField(max_length=10, default='Recipient')
    # availability = models.CharField(max_length=30, choices=availability_choices)

    
    # availability = models.CharField(max_length=20, choices=availability_choices)
    # password = models.CharField(max_length=128)
    # user_type = models.CharField(max_length=10, default='Recipient')

    # class Meta:
    #     verbose_name = "Recipient"
    #     verbose_name_plural = "Recipients"

    # def __str__(self):
    #     return self.username


# class User(models.Model):

    # donor = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    # username = models.CharField(max_length=50)            
    # first_name = models.CharField(max_length=30)
    # last_name = models.CharField(max_length=30)
    # dob = models.DateField()
    # email = models.CharField(max_length=50)
    # photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    # city = models.CharField(max_length=30)
    # blood_type = models.CharField(max_length=30,default="A+")
    # user_type = models.CharField(max_length=10, default='Donor')
    # availability = models.CharField(max_length=20, choices=availability_choices)
    # gender = models.CharField(max_length=1, choices=gender_choices)

    # def __str__(self):
    #     return self.username
    
class BloodDonationBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"Blood Donation Booking for {self.first_name} {self.last_name}"