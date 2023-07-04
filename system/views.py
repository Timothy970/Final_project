import json
import queue
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponseRedirect, JsonResponse
from .forms import LoginForm1, UserRegistrationForm, UserEditForm, ProfileEditForm, BloodDonationForm, ProfileForm, BloodRequestForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404 
from django.contrib.auth.models import User
from .models import Profile, DonationSchedule, Message, BloodDonationBooking, Donation_Made
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
# from channels.layers import get_channel_layer
from django.db.models import Q, F
# from .consumers import ChatConsumery
from .forms import BloodRequestForm
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from .models import Notification, BloodRequest
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.views.generic import ListView
from django.utils import timezone
from django.utils.timezone import get_current_timezone
from asgiref.sync import async_to_sync
from django.conf import settings
from wkhtmltopdf.views import PDFTemplateView





# Create your views here.
def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def learnmore(request):
    template = loader.get_template('learnmore.html')
    return HttpResponse(template.render())

def login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

# def loginrecipient(request):
    template = loader.get_template('registration/loginrecipient.html')
    return HttpResponse(template.render())
def signin(request):
    template = loader.get_template('signin.html')
    return HttpResponse(template.render())

def signinrequest(request):
    template = loader.get_template('signinrequest.html')
    return HttpResponse(template.render())
def terms(request):
    template = loader.get_template('terms.html')
    return HttpResponse(template.render())

def notification(request):
    template = loader.get_template('notifications.html')
    return HttpResponse(template.render())

def blood_request_confirmed(request):
    template = loader.get_template('blood_request_confirmed.html')
    return HttpResponse(template.render())

def user_login(request):
        
    if request.method == 'POST':
        
        form = LoginForm1(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                            username=cd['username'],
                            password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfuly')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm1()
    return render(request, 'login.html', {'form': form})  
    
# def recipient_login(request):
        
    if request.method == 'POST':
        
        form = LoginRecipientForm1(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                            username=cd['username'],
                            password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfuly')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginRecipientForm1()
    return render(request, 'recipientlogin.html', {'form': form})      


@login_required
def dashboard(request):
    return render(request,
                  'dashboard.html',
                  {'section': 'dashboard'})      
    
def confirm(request):
    return render(request,
                  'blood_confirmed.html',
                  {'section': 'confirm'}) 
def register(request):
    
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        
        if user_form.is_valid():
 # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            
          
 # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request,
                          'register_done.html',
                          {'new_user': new_user})

    else:
        user_form = UserRegistrationForm()
        
    return render(request, 'register.html', {'user_form': user_form})

# def recipientregister(request):
    
#     if request.method == 'POST':
#         user_form = RecipientRegistrationForm(request.POST)
#         if user_form.is_valid():
#  # Create a new user object but avoid saving it yet
#             new_user = user_form.save(commit=False)
#  # Set the chosen password
#             new_user.set_password(user_form.cleaned_data['password'])
#             new_user.save()
#             return render(request,
#                           'register_done.html',
#                           {'new_user': new_user})
#  # Save the User object
#             # new_user.save()
#             # Donors.objects.create(user=new_user)
#             # return render(request, 'register_done.html', {'new_user': new_user})
#     else:
#         user_form = RecipientRegistrationForm()
#     return render(request, 'recipientregister.html', {'user_form': user_form})

# idk
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('dashboard')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    whatsapp_link = None

    if profile_form.is_valid():
        whatsapp_link = profile_form.get_whatsapp_link()

    return render(request, 'edit.html', {'user_form': user_form, 'profile_form': profile_form, 'whatsapp_link': whatsapp_link})            

# display user details
def user_details(request, user_id):
    if request.user.id != user_id:
        user = Profile.objects.get(id=user_id)
        data = {
            "username": user.user.username,
            "first_name": user.user.first_name,
            "last_name": user.user.last_name,
            "email": user.user.email,
            "date_of_birth": user.date_of_birth,
            "photo": user.photo,
            "availability": user.availability,
            "gender": user.gender,
            "blood_type": user.blood_type,
            "city": user.city,
        }
        return render(request, "dashboard.html", data)
    else:
        return render(request, "forbidden.html")
    
def view_profiles(request):
    current_user_profile = request.user.profile
    profiles = Profile.objects.exclude(user=request.user)
    for profile in profiles:
        profile.whatsapp_link = profile.get_whatsapp_link()
        print(f"WhatsApp link for {profile.user.username}: {profile.whatsapp_link}")

    context = {
        'current_user_profile': current_user_profile,
        'profiles': profiles
    }
    print(context)
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def my_view(request):
    if request.user.user_type == 'Donor':
        return render(request, 'home.html')
    elif request.user.user_type == 'Recipient':
        return render(request, 'dashboard.html')
    else:
        return render(request, 'error.html')
    
#Schedule view
@login_required
def view_bookings(request):
    bookings = BloodDonationBooking.objects.filter(user=request.user)
    return render(request, 'schedule.html', {'bookings': bookings})

def delete_booking(request, booking_id):
    booking = get_object_or_404(BloodDonationBooking, pk=booking_id)
    if request.method == "POST":
        booking.delete()
        
    return redirect('schedule')

@login_required
def blood_donation_booking(request):
    confirmation_message = None
    if request.method == 'POST':
        form = BloodDonationForm(request.POST, user=request.user)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()

            # Additional logic for blood donation booking
            # ...
            confirmation_message = "Booked successfully"

            return redirect('dashboard')
    else:
        form = BloodDonationForm(user=request.user)
    
    
    
    return render(request, 'book_appointment.html', {'form': form, 'confirmation_message': confirmation_message})


#blood request
def blood_request(request):
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            blood_request = form.save()
            send_notification_email(blood_request)
            return redirect('confirm')
    else:
        form = BloodRequestForm()
    return render(request, 'emergency.html', {'form': form})


def send_notification_email(blood_request):
    subject = 'Blood Request Notification'
    template_data ={
        'greeting': 'Hello blood hero,',
        'blood_request': blood_request,
        'info': 'Please if you are available and match the specified blood type, you can avail yourself and save a life.',
    }
    html_message = render_to_string('email_templates/blood_request.html', template_data)
    plain_message = strip_tags(html_message)
    from_email = 'webbasedblooddonation@gmail.com'
    recipient_list = list(User.objects.values_list('email', flat=True))
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
    #website notification


# @login_required
# def notifications(request):
#     notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
#     return render(request, 'notifications.html', {'notifications': notifications})

# def blood_request_details(request, notification_id):
#     notification = get_object_or_404(Notification, id=notification_id)
#     form = BloodRequestForm(instance=notification.blood_request)
#     return render(request, 'blood_request_details.html', {'form': form})
def blood_request_count(request):
    count = BloodRequest.objects.count()
    data = {
        'count': count,
    
    }
    return JsonResponse(data)

def blood_request_list(request):
    current_time = timezone.now()
    blood_requests = BloodRequest.objects.annotate(
        expiration_time=F('created_at') + timezone.timedelta(days=1)
        ).filter(expiration_time__gt=current_time)
    return render(request, 'blood_requests.html', {'blood_requests': blood_requests})


#donations made report

def donation_report(request):
    donations = Donation_Made.objects.filter(donor=request.user).order_by('-date')
    total_points = sum((donation.points_earned for donation in donations))
    return render(request, 'donation_report.html', {'donations': donations, 'total_points': total_points})

class DonationReportPDF(PDFTemplateView):
    template_name = 'donation_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['donations'] = Donation_Made.objects.filter(donor=self.request.user).order_by('-date')
        return context

    def get_filename(self):
        return 'donation_report.pdf'
    
def reward_certificate(request):
    donations = Donation_Made.objects.filter(donor=request.user).order_by('-date')
    total_points = sum(donation.points_earned for donation in donations)

    if total_points >= 400:
        certificate_type = 'platinum'
    elif total_points >= 200:
        certificate_type = 'gold'
    elif total_points >= 100:
        certificate_type = 'silver'
    elif total_points >= 50:
        certificate_type = 'bronze'
    else:
        return HttpResponse('Sorry, you have not earned enough points for a certificate yet.')

    certificate_data = {'recipient_name': request.user.username, 'certificate_type': certificate_type}
    certificate_html = render_to_string('certificate.html', certificate_data)
    pdf_file = PDFTemplateView.as_pdf(template_name='certificate.html', context=certificate_data)
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{request.user.username}_certificate.pdf"'
    return response


from django.contrib.auth.models import User
from django.shortcuts import render

def user_report(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'user_report.html', context)
