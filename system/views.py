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
from .forms import BloodRequestForm, MessageForm
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from .models import Notification, BloodRequest, Message, Chat
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.views.generic import ListView
from django.utils import timezone
from django.utils.timezone import get_current_timezone
from asgiref.sync import async_to_sync
from django.conf import settings
from wkhtmltopdf.views import PDFTemplateView
from django.contrib import messages
from django.db.models import Max, Count, Q
import logging
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_datetime
# logger = logging.getLogger('myapp')
from .utils import get_or_create_1to1_chat


User = get_user_model()
PAGE_SIZE = 20


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
            Profile.objects.create(
                user=new_user,
                date_of_birth=user_form.cleaned_data['date_of_birth'],
                phone_number=user_form.cleaned_data['phone_number'],
                city=user_form.cleaned_data['city'],
                blood_type=user_form.cleaned_data['blood_type'],
                availability=user_form.cleaned_data['availability'],
                gender=user_form.cleaned_data['gender']
            )
            return render(request,
                          'dashboard.html',
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
            messages.success(request, "Your blood request has been submitted successfully.")
            return redirect('emergency') 
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


@login_required
def chat_view(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    messages = Message.objects.filter(
        sender__in=[request.user, receiver],
        receiver__in=[request.user, receiver]
    )
    form = MessageForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        new_message = form.save(commit=False)
        new_message.sender = request.user
        new_message.receiver = receiver
        new_message.save()
        return redirect('chat_view', user_id=receiver.id)
    
    return render(request, 'chat/chat.html', {
        'receiver': receiver,
        'messages': messages,
        'form': form
    })

@login_required
def chat_list(request, user_id=None):
    chats = (
        Chat.objects.filter(participants=request.user)
        .annotate(latest_message_time=Max("messages__timestamp"))
        .order_by("-latest_message_time")
        .distinct()
    )

    chat_rows = []
    seen = set()
    for chat in chats:
        other = chat.participants.exclude(id=request.user.id).first()
        if not other or other.id in seen:
            continue
        seen.add(other.id)
        latest = chat.messages.order_by('-timestamp').first()
        unread_count = chat.messages.filter(is_read=False, reciever=request.user).count()
        chat_rows.append({
            "chat": chat,
            "other": other,
            "latest_message": latest,
            "unread_count": unread_count
        })

    context = {"chats": chat_rows}

    if user_id:
        other_user = get_object_or_404(User, id=user_id)
        context["open_user_id"] = other_user.id
        context["open_user_name"] = other_user.username

    return render(request, "chat_list.html", context)


@login_required
def chat_messages_api(request, user_id):
    """
    GET: Return JSON messages for chat between request.user and user_id.
    Query params:
      - before: ISO datetime string (returns messages older than this timestamp)
    """
    if request.method != "GET":
        return HttpResponseBadRequest("Only GET allowed")

    current_user = request.user
    other_user = get_object_or_404(User, id=user_id)

    # Get only messages between these two users
    qs = Message.objects.filter(
        Q(sender=current_user, reciever=other_user) |
        Q(sender=other_user, reciever=current_user)
    ).order_by('-timestamp')

    before = request.GET.get('before')
    if before:
        before_dt = parse_datetime(before)
        if before_dt:
            qs = qs.filter(timestamp__lt=before_dt)

    messages_page = list(qs[:PAGE_SIZE])

    messages_data = [
        {
            "id": m.id,
            "is_mine": m.sender_id == current_user.id,  # True if I sent it
            "sender_id": m.sender_id,
            "sender_username": m.sender.username,
            "content": m.content,
            "timestamp": m.timestamp.isoformat(),
        }
        for m in reversed(messages_page)  # reverse to oldest→newest
    ]

    return JsonResponse({
        "messages": messages_data,
        "has_more": qs.count() > PAGE_SIZE
    })


@login_required
def mark_read_api(request, user_id):
    """Mark messages in chat from other_user to request.user as read."""
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")

    other_user = get_object_or_404(User, id=user_id)
    chat, _ = get_or_create_1to1_chat(request.user, other_user)

    updated = chat.messages.filter(reciever=request.user, is_read=False).update(is_read=True)
    return JsonResponse({"marked": updated})


@login_required
def chat_detail(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    # Find existing chat between both users
    chat = Chat.objects.filter(participants=request.user)\
                       .filter(participants=other_user)\
                       .annotate(num_participants=Count('participants'))\
                       .filter(num_participants=2)\
                       .first()

    # If not found, create a new one
    if not chat:
        chat = Chat.objects.create(created_at=timezone.now())
        chat.participants.add(request.user, other_user)

    messages = Message.objects.filter(chat=chat).order_by('timestamp')

    return render(request, 'chat_detail.html', {
        'chat': chat,
        'messages': messages,
        'receiver': other_user,
        'user_id': other_user.id
    })