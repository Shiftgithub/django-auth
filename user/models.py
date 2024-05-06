from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('user', 'User'),
    )

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('pending', 'Pending'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_info", null=True)
    nid = models.CharField(max_length=255)
    ph_no = models.CharField(max_length=255)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    address = models.TextField()


class VerifyOtp(models.Model):
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='varify_otp', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=False, null=True)
    deleted_at = models.DateTimeField(auto_now=False, null=True)


