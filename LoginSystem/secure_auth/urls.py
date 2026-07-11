from django.shortcuts import render
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_step1_view, name='signup_step1'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('resend-otp/', views.resend_otp_view, name='resend_otp'),
    path('activate-account/', views.activate_password_view, name='activate_password'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    path('customer-zone/', views.customer_zone_view, name='customer_zone'),
    path('agent-zone/', views.agent_zone_view, name='agent_zone'),
    path('admin-zone/', views.admin_zone_view, name='admin_zone'),

]