from django.core.management.base import BaseCommand
from .models import Profile

gender_choices = [
   ('M', 'Male'),
   ('F', 'Female'),
   ('O', 'Other')  
]
Profile.objects.update_choices('gender', gender_choices)   

