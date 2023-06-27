import queue
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponseRedirect, JsonResponse
from .forms import LoginForm1, UserRegistrationForm, UserEditForm, ProfileEditForm, BloodDonationForm, ProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404 
from django.contrib.auth.models import User
from .models import Profile, DonationSchedule, Message, BloodDonationBooking
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
# from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Q
# from .consumers import ChatConsumer
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
    return render(request, 'edit.html', {'user_form': user_form, 'profile_form': profile_form})            

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
    context = {
        'current_user_profile': current_user_profile,
        'profiles': profiles
    }
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


# #chatting

def chat(request, user_id):
    reciever = get_object_or_404(User, id=user_id)
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(reciever=reciever)) |
        (Q(sender=reciever) & Q(reciever=reciever))
    ).order_by('timestamp')
    
    context = {
        'reciever': reciever,
        'messages': messages
    }
    return render(request, 'chat.html', context)

def send_message(request):
    if request.method == 'POST' and request.is_ajax():
        reciever_id = request.POST.get('reciever_id')
        content = request.POST.get('content')
        
        reciever = get_object_or_404(User, id=reciever_id)
        
        message = Message.objects.create(
            sender=request.user,
            reciever=reciever,
            content=content
        )
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})