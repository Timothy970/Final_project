from django.contrib import admin
from .models import Donors 
# Register your models here.
@admin.register(Donors)
class DonorsAdmin(admin.ModelAdmin):
    list_display = ['user','fname','lname','dob','email','photo','city','blood_type','availability']
    raw_id_fields = ['user']
