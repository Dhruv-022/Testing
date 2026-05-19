from django.contrib import admin
from django.urls import path, include
from analytics.views import home
from django.views.generic import TemplateView  # 1. Import TemplateView

urlpatterns = [
    # Fixed the admin path
    path('admin/', admin.site.urls),
    
    # This includes your visitor counter logic
    path('api/', include('analytics.urls')),
    
    # Your home page
    path('', home, name='home'),
    
    # 2. ADD THIS LINE: Tells Django to match 'contact/index.html' and serve your file
    path('contact/index.html', TemplateView.as_view(template_name="contact/index.html"), name='contact_page'),
]