from django.urls import path
from .views import log_visit

urlpatterns = [
    # This creates the endpoint: /api/log-visit/
    path('log-visit/', log_visit, name='log_visit'),
]