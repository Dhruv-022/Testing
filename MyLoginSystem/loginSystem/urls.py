from django.contrib import admin
from django.urls import path, include # <── Make sure include is imported here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('secure_auth.urls')), # <── Redirects all root traffic to our application router
]