from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.timezone import now

from time import time
from pyotp import random_base32, TOTP
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    username = PhoneNumberField(unique=True)
    key = models.CharField(max_length=16, default=random_base32)
    REQUIRED_FIELDS = []

    def verify_otp(self, otp: str) -> bool:
        if not otp:
            return False

        try:
            return TOTP(self.key, interval=settings.OTP_EXPIRE_TIME).verify(otp, for_time=self.otp.otp_at)
        except:
            return False

class UserOtp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='otp')
    otp_at = models.DateTimeField(default=now)
    class Meta:
        managed = True
        db_table = 'user_otp'