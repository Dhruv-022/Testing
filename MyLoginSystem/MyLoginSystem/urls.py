from django.contrib import admin
from django.urls import path
from .views import catch_url_data_view # <── We will write this function next

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test-gate/', catch_url_data_view), # <── This is the path the browser will target
]