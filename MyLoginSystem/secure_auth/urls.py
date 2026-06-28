from django.urls import path
from .views import signup_view, verify_otp_view # <── Import the new view function
from django.http import HttpResponse

urlpatterns = [
    path('signup/', signup_view),
    path('verify-otp/', verify_otp_view), # <── Connected directly to our verification view engine!
    
    # Simple placeholder route to prove the account unlocked successfully
    path('login-success/', lambda request: HttpResponse("<h1>🎉 Account successfully verified and activated!</h1>")),
]