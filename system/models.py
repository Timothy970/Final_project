from django.db import models
from django.conf import settings

# Create your models here.
class Donors(models.Model):
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE)
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    dob = models.DateField()
    email = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    city = models.CharField(max_length=30)
    blood_type = models.CharField(max_length=30)
    availability = models.CharField(max_length=30)
    
    def __str__(self):
        return f'Donors of {self.user.username}'
 
   