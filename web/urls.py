from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('about_us/', views.about_us_view, name='about_us'),
    path('music/', views.base_music_view, name='music'),
    path('info/', views.base_info_view, name='info'),
] 