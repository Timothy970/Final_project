from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponseRedirect
from .forms import LoginForm1, UserRegistrationForm, UserEditForm, DonorsEditForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Donors

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

def signin(request):
    template = loader.get_template('signin.html')
    return HttpResponse(template.render())

def signinrequest(request):
    template = loader.get_template('signinrequest.html')
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
                return HttpResponse('Invalig login')
    else:
        form = LoginForm1()
    return render(request, 'login.html', {'form': form})      

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
 # Save the User object
            new_user.save()
            Donors.objects.create(user=new_user)
            return render(request, 'register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})

# idk
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        donor_form = DonorsEditForm(instance=request.user.donors, data=request.POST, files=request.FILES)
        if user_form.is_valid() and donor_form.is_valid():
            user_form.save()
            donor_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        donor_form = DonorsEditForm(instance=request.user.donors)
    return render(request, 'edit.html', {'user_form': user_form, 'donor_form': donor_form})            