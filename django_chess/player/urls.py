from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/',auth_views.LoginView.as_view(template_name = 'player/login.html'), name = 'login'),
    path('signup/', views.signup,  name='signup'),
    path('profile/', views.profile,  name='profile'),
    path('logout/', views.logout_view,  name='logout')
]