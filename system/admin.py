from django.contrib import admin
from .models import Profile, BloodDonationBooking, Donation_Made
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse
from django.utils.html import format_html
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo','availability','gender', 'blood_type', 'city','phone_number', 'user_report_link']
    raw_id_fields=['user']

    def user_report_link(self, obj):
        url = reverse('system:user_report')
        link = format_html('<a href="{}?user={}&date_of_birth={}&availability={}&gender={}&blood_type={}&city={}&phone_number={}&first_name={}&last_name={}">Generate Report</a>',
                           url,
                           obj.user.username,
                           obj.date_of_birth,
                           obj.availability,
                           obj.gender,
                           obj.blood_type,
                           obj.city,
                           obj.phone_number,
                           obj.user.first_name,
                           obj.user.last_name)
        return link
    user_report_link.short_description = 'Report'
    
@admin.register(BloodDonationBooking)
class BloodDonationBookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'date', 'time']
    raw_id_fields = ['user']

@admin.register(Donation_Made)
class Donation_MadeAdmin(admin.ModelAdmin):
    list_display = ['donor', 'date', 'location', 'blood_type', 'quantity', 'notes', 'points_earned']


class UserAdmin(admin.ModelAdmin):    
   
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'user_report_link')

    def user_report_link(self, obj):
        url = reverse('system:user_report')
        link = format_html('<a href="{}?user={}&is_staff={}">All Users</a>',
                            url,
                            obj.username,
                            obj.is_staff)
        return link
    user_report_link.short_description = 'User Report'

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Profile)
admin.site.register(Profile, ProfileAdmin)
