from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserRegistrationForm(forms.Form):
    # 1. Define the input fields the user must fill out
    username = forms.CharField(max_length=15, min_length=3)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(), min_length=8)

    # 2. Add a custom security check to protect the system
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        # Custom Guardrail: Prevent the user from setting their password to their username
        if username and password and username.lower() in password.lower():
            raise ValidationError("Security Error: Password cannot contain your username!")
            
        return cleaned_data
    

class OTPVerificationForm(forms.Form):
    # A single field designed strictly to capture the 6 digit payload characters
    otp_code = forms.CharField(max_length=6, min_length=6, label="Enter 6-Digit OTP")