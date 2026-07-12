from django.db import models

class UserAccount(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', 'Institution Admin'),
        ('SUPERVISOR', 'Support Agent / Supervisor'),
        ('STANDARD', 'Customer / Standard User'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255, blank=True, null=True)
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    active_status = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)

    # 🌟 2. Add the Role Column (Defaults to STANDARD automatically)
    role = models.CharField(
        max_length=15,
        choices=ROLE_CHOICES,
        default='STANDARD'
    )
    def __str__(self):
        return f"{self.first_name} \n{self.last_name} \n{self.email} \nVerified: {self.email_verified} \nActive: {self.active_status} \n"