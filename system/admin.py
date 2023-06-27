from django.contrib import admin
from .models import Profile, BloodDonationBooking

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo','availability','gender', 'blood_type', 'city','phone_number']
    raw_id_fields=['user']
    
@admin.register(BloodDonationBooking)
class BloodDonationBookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'date', 'time']
    raw_id_fields = ['user']
# from .models import Profile
# Register your models here.
# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ['user','date_of_birth', 'photo']
#     raw_id_fields = ['user']
# @admin.register(User)

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
    # list_display = ['username','first_name', 'last_name', 'email', 'dob', 'gender', 'city', 'availability','photo','blood_type','user_type']
    # raw_id_fields = ['username']
    

    
# @admin.register(Recipient)
# class RecipientAdmin(admin.ModelAdmin):
    # list_display = ['username','first_name', 'last_name', 'email','gender']
    # raw_id_fields = ['username']    