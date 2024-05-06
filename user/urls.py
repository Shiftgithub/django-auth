from . import views
from django.urls import path


urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register_user, name='register'),
    path('otp/setup/', views.verify_otp, name='otp_setup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
]

