from django import forms
from django.contrib.auth.models import User
from .models import Donors

class LoginForm1(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
 
class UserRegistrationForm(forms.ModelForm):
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
    
    password = forms.CharField(label='Password', widget=forms.PasswordInput) 
    password2 = forms.CharField(label='Confirmed password', widget=forms.PasswordInput)
    last_name = forms.CharField(label='Last Name')
    dob = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=gender_choices, required=True)
    city = forms.ChoiceField(choices=city_choices, required=True)
    availability = forms.ChoiceField(choices=availability_choices, required=True)
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text=None    
    
    class Meta:
        
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'dob', 'gender', 'city', 'availability']
        
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
    
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User    
        fields = ['username', 'first_name', 'email']
        
    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id).filter(email=data)    
        if qs.exists():
            raise forms.ValidationError('Email already in use.')
        return data

class DonorsEditForm(forms.ModelForm):
    class Meta:
        model = Donors
        fields =['user','fname','lname','dob','email','photo','city','blood_type','availability']
        
        