from django.db import models
from django.contrib.auth.models import User

class OTPRecord(models.Model):
    # 1. Link this record directly to a specific User row in the database.
    # If the user account is deleted, delete this OTP row automatically (on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # 2. Store the 6-digit numeric string characters code
    code = models.CharField(max_length=6)
    
    # 3. Automatically record the exact date and time this row was created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP for {self.user.username}: {self.code}"