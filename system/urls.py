from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('learnmore/', views.learnmore, name='learnmore'),
    path('login/', views.login, name='login')
]
