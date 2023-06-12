from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('learnmore/', views.learnmore, name='learnmore'),
    # path('login/', views.user_login, name='login'),
    path('signin/', views.signin, name='signin'),
    path('signinrequest/', views.signinrequest, name='signinrequest'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name ='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('changepassword/', auth_views.PasswordChangeView.as_view(), name='changepassword'),
    path('passwordchanged/', auth_views.PasswordChangeView.as_view(), name='passwordchanged'),
    
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete',),
    
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
]
