from typing import Any, Dict
from django import forms
from django.contrib.auth.models import User
import datetime
from django.forms import ValidationError
from .models import Profile, BloodDonationBooking
import phonenumbers
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# from.phonenumbers.phonenumberutil import PhoneNumberFormat
from .models import BloodRequest
from .models import Message


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
class LoginForm1(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class LoginRecipientForm1(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
 
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    names = forms.CharField(label='Full Name', max_length=100)

    # Profile fields
    date_of_birth = forms.DateField(label='Date of Birth', widget=forms.DateInput(attrs={'type': 'date'}))
    phone_number = forms.CharField(label='Phone Number')
    city = forms.ChoiceField(choices=Profile._meta.get_field('city').choices)
    blood_type = forms.ChoiceField(choices=Profile._meta.get_field('blood_type').choices)
    availability = forms.ChoiceField(choices=Profile._meta.get_field('availability').choices)
    gender = forms.ChoiceField(choices=Profile._meta.get_field('gender').choices)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        validate_age(dob)
        return dob
    # def clean_dob(self):
    #     dob = self.cleaned_data['dob']
    #     if dob < datetime.date(1997, 1, 1):
    #         raise ValidationError('The user must be atleast 16 years old')
    #     return dob

def validate_age(value):
    today = date.today()
    age_limit = today - timedelta(days=16 * 365)
    if value > age_limit:
        raise ValidationError(
            _('You must be 16 years or older'),
            params={'value': value},
        )
        
class UserEditForm(forms.ModelForm):
    
    class Meta:
        model = User    
        fields = ['first_name', 'last_name', 'email']
        
    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id).filter(email=data)    
        if qs.exists():
            raise forms.ValidationError('Email already in use.')
        return data


class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo','availability','gender', 'blood_type', 'city', 'phone_number']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number:
            raise forms.ValidationError('Phone number is required')
        return phone_number

    def get_whatsapp_link(self):
        if self.is_valid():
            cleaned_data = self.cleaned_data
            phone_number = cleaned_data.get('phone_number')

            if phone_number:
                whatsapp_number = f"{phone_number}"
                return f"https://api.whatsapp.com/send?phone={whatsapp_number}"
        return None

class RecipientRegistrationForm(forms.ModelForm): 
    password = forms.CharField(label='Password', widget=forms.PasswordInput) 
    password2 = forms.CharField(label='Confirmed password', widget=forms.PasswordInput)
    last_name = forms.CharField(label='Last Name')    
    gender = forms.ChoiceField(choices=gender_choices, required=True)
    
    
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text=None   
        initial = {} 
        for field in self.Meta.fields:
            initial[field] = ''
        self.initial=initial    
    
    class Meta:
        
        model = User
        fields = ['username', 'first_name', 'last_name', 'email','gender']
        
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']    
    
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data
            
from django.forms.widgets import Select

class HourIntervalSelectWidget(Select):
    def __init__(self, attrs=None):
        intervals = [
            ("08:00", "08:00 AM"),
            ("09:00", "09:00 AM"),
            ("10:00", "10:00 AM"),
            ("11:00", "11:00 AM"),
            ("12:00", "12:00 PM"),
            ("13:00", "1:00 PM"),
            ("14:00", "2:00 PM"),
            ("15:00", "3:00 PM"),
            ("16:00", "4:00 PM"),
            # Add more hour intervals as needed
        ]
        super().__init__(attrs, choices=intervals)   


class BloodDonationForm(forms.ModelForm):
    
    first_name = forms.CharField(required=True, label='First Name')
    last_name = forms.CharField(required=True, label='Last Name')
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=HourIntervalSelectWidget)
    
    class Meta:
        model = BloodDonationBooking
        fields = ['first_name', 'last_name', 'date', 'time']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get("user")
        selected_date = cleaned_data.get('date')
        if selected_date and selected_date <= date.today():
            raise forms.ValidationError("Please select a date in the future.")
        
        user = self.initial.get('user')
        existing_booking = BloodDonationBooking.objects.filter(user=user)
        if existing_booking.exists() > 1:
            raise forms.ValidationError("You already have a booking.")
        
        return cleaned_data
        
    # def clean(self):
    #     cleaned_data = super().clean()
    #     user = self.initial.get('user') 
    #     existing_booking = BloodDonationBooking.objects.filter(user=user)
    #     if existing_booking.exists():
    #             raise forms.ValidationError("You already have a booking")
    #     return cleaned_data

class ProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    photo = forms.ImageField()
    availability = forms.CharField(max_length=200)
    gender = forms.CharField(max_length=100)
    blood_type = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    
    
    
    class Meta:
        model = Profile
        fields = ['photo','availability','gender', 'blood_type', 'city', 'phone_number']
        
    # Blood request form
class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['first_name', 'last_name', 'blood_type', 'contact_number', 'location']
    


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'Type your message...'})
        }
