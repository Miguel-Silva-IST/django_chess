from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('play/', views.play, name='play'),
    path('accounts/', include('django.contrib.auth.urls')),
    path("favicon.ico", views.favicon, name='favicon'),
    path("sandbox/", views.sandbox, name='sandbox'),
    path('move/', views.move, name='test'),
    path('end_game/', views.end_game, name='end_game'),
    path('time_travell/', views.time_travell, name='time_travell')
]
