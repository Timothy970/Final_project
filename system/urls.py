from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
# from system.routing import websocket_urlpatterns
app_name = 'system'
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
    # path('recipientregister/', views.recipientregister, name='recipientregister'),
    # path('loginrecipient/', auth_views.LoginView.as_view(), name='loginrecipient'),
    path('terms/', views.terms, name='terms'),
    
    path('schedule/', views.view_bookings, name='schedule'),
    path('bookings/delete/<int:booking_id>/', views.delete_booking, name='delete_booking',),
    path('book/', views.blood_donation_booking, name='book_appointment'),
    path('profiles/', views.view_profiles, name='view_profiles'),
    
    path('request/', views.blood_request, name='emergency'),
    path('confirm', views.confirm, name='confirm'),
    # path('notifications/', views.notification, name='notifications'),
    # path('notifications/<int:notification_id>/details', views.blood_request_details, name='blood_request_details'),
    path('blood_request_count/', views.blood_request_count, name='blood_request_count'),
    path('blood_requests/', views.blood_request_list, name='blood_requests'),

    path('donation_report/', views.donation_report, name='donation_report'),
    path('donation_report_pdf/', views.DonationReportPDF.as_view(), name='donation_report_pdf'),
    path('reward_certificate/', views.reward_certificate, name='reward_certificate'),
    path('user_report/', views.user_report, name='user_report'),
]