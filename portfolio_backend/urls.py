from django.contrib import admin
from django.urls import path, include # Add 'include' here

urlpatterns = [
    path('admin/', admin.get_id()),
    path('api/', include('analytics.urls')), # Add this line
]