import random
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from .models import OTPRecord
from .forms import OTPVerificationForm

def signup_view(request):
    # Personality A: The user is submitting data payload
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        
        # Trigger the forms.py security firewall checks
        if form.is_valid():
            # 1. Extract the clean, validated text strings from the form dictionary
            extracted_username = form.cleaned_data['username']
            extracted_email = form.cleaned_data['email']
            extracted_password = form.cleaned_data['password']
            
            # 2. Create the User row in a strict hidden pending state
            new_user = User.objects.create_user(
                username=extracted_username,
                email=extracted_email,
                password=extracted_password
            )
            new_user.is_active = False # <── CRITICAL GUARD: Account is locked!
            new_user.save()
            
            # 3. OTP Engine: Generate a random 6-digit numeric string characters code
            generated_otp = str(random.randint(100000, 999999))
            
            # 4. State Storage: Save the code to our tracking model database table
            otp_entry = OTPRecord(user=new_user, code=generated_otp)
            otp_entry.save()
            
            # 5. Terminal Debug Wire: Print the code directly to our running backend console
            # In a production system, this string would be fired out via an Email API wire.
            # For our development fortress, we will read it directly from our terminal!
            print("\n" + "="*50)
            print("📡 OUTBOUND IDENTITY OTP SIMULATOR DISPATCHED!")
            print(f"Target Inbox: {extracted_email}")
            print(f"Generated Code Cargo: {generated_otp}")
            print("="*50 + "\n")
            
            # 6. Redirect the browser tab container to the next intermediate verification path
            return redirect('/verify-otp/')
            
    # Personality B: The initial load vector (GET)
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