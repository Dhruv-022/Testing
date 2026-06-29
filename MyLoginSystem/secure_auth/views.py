import random
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from .models import OTPRecord
from .forms import OTPVerificationForm

import random
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail # <── 1. CRITICAL: Add this import at the top!
from .forms import UserRegistrationForm
from .models import OTPRecord

def signup_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        
        if form.is_valid():
            extracted_username = form.cleaned_data['username']
            extracted_email = form.cleaned_data['email']
            extracted_password = form.cleaned_data['password']
            
            new_user = User.objects.create_user(
                username=extracted_username,
                email=extracted_email,
                password=extracted_password
            )
            new_user.is_active = False 
            new_user.save()
            
            generated_otp = str(random.randint(100000, 999999))
            
            otp_entry = OTPRecord(user=new_user, code=generated_otp)
            otp_entry.save()
            
            # 2. REAL NETWORK DISPATCH: Blast the email across the internet!
            email_subject = "🔑 Your Identity Verification OTP"
            email_body = f"Welcome to the Fortress!\n\nYour 6-digit verification code is: {generated_otp}\n\nThis code will expire shortly."
            
            send_mail(
                subject=email_subject,
                message=email_body,
                from_email=None, # <── This automatically tells Django to pull DEFAULT_FROM_EMAIL from settings.py
                recipient_list=[extracted_email], # <── Sends straight to the user's input email
                fail_silently=False, # <── If Brevo rejects it, throw a clear error on screen so we can debug it!
            )
            
            return redirect('/verify-otp/')
            
    else:
        form = UserRegistrationForm()
        
    basket = {
        'form_blueprint': form,
    }
    return render(request, 'signup.html', basket)





def verify_otp_view(request):
    error_message = None

    # Personality A: The user submits the 6 digits
    if request.method == "POST":
        form = OTPVerificationForm(request.POST)
        
        if form.is_valid():
            # 1. Extract the typed 6 digits from the form package
            typed_code = form.cleaned_data['otp_code']
            
            try:
                # 2. Search our database table to find a matching code row
                otp_record = OTPRecord.objects.get(code=typed_code)
                
                # 3. Pull the connected user object using the Foreign Key pointer link!
                pending_user = otp_record.user
                
                # 4. Flip the security flag to unlock the account
                pending_user.is_active = True
                pending_user.save()
                
                # 5. Database Cleanup: Delete the OTP row so it cannot be reused
                otp_record.delete()
                
                # 6. Success Route Redirect: Send them to a clean login screen placeholder
                return redirect('/login-success/')
                
            except OTPRecord.DoesNotExist:
                # Security Protection Guard: Triggered if the code isn't in our table
                error_message = "Security Rejection: Invalid or expired OTP code!"
                
    # Personality B: Initial load vector (GET)
    else:
        form = OTPVerificationForm()

    basket = {
        'form_blueprint': form,
        'error_container': error_message
    }
    return render(request, 'verify_otp.html', basket)