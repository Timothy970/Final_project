from typing import Any, Dict
from django import forms
from django.contrib.auth.models import User
import datetime
from django.forms import ValidationError
from .models import Profile, BloodDonationBooking
# import phonenumbers
# from.phonenumbers.phonenumberutil import PhoneNumberFormat
# from phonenumbers import parse, is_valid_number

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
    password2 = forms.CharField(label='Confirmed password', widget=forms.PasswordInput)
    last_name = forms.CharField(label='Last Name')
    # dob = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    # gender = forms.ChoiceField(choices=gender_choices, required=True)
    # city = forms.ChoiceField(choices=city_choices, required=True)
    # availability = forms.ChoiceField(choices=availability_choices, required=True)
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text=None   
        initial = {} 
        for field in self.Meta.fields:
            initial[field] = ''
        self.initial=initial    
    
    class Meta:
        
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        
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
    
    # def clean_dob(self):
    #     dob = self.cleaned_data['dob']
    #     if dob < datetime.date(1997, 1, 1):
    #         raise ValidationError('The user must be atleast 16 years old')
    #     return dob
    
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
        fields = ['date_of_birth', 'photo','availability','gender', 'blood_type', 'city']
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
            
            
from django import forms

class BloodDonationForm(forms.ModelForm):
    first_name = forms.CharField(required=True, label='First Name')
    last_name = forms.CharField(required=True, label='Last Name')
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    
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
        user = self.initial.get('user')
        if user or BloodDonationBooking.objects.filter(user=user).exists():
            raise forms.ValidationError("You already have a booking.")
        return cleaned_data

class ProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    photo = forms.ImageField()
    availability = forms.CharField(max_length=200)
    gender = forms.CharField(max_length=100)
    blood_type = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    
    phone_number = forms.CharField(max_length=20, min_length=10)
    
    class Meta:
        model = Profile
        fields = ['photo','availability','gender', 'blood_type', 'city', 'phone_number']
        
    # def clean_phone_number(self):
    #     phone_number = self.cleaned_data['phone_number']
    #     parsed_number = parse(phone_number, 'ZZ')
    #     if not is_valid_number(parsed_number):
    #         raise forms.ValidationError('Invalid phone number.')
    #     return phone_number    