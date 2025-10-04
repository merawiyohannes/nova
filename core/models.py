from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('doctor', 'Doctor'),
        ('receptionist', 'Receptionist'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.username} ({self.user_type})"

class Client(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    
    # Basic Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    # Doctor's Notes
    diagnosis = models.TextField(blank=True)
    treatment_plan = models.TextField(blank=True)
    prescriptions = models.TextField(blank=True)
    doctor_notes = models.TextField(blank=True)
    
    # Timestamps
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='clients_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_visited = models.DateTimeField(null=True, blank=True)
    
    # Referral Information
    referred_to = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='referred_clients',
        limit_choices_to={'user_type': 'doctor'}
    )
    REFERRAL_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    referral_status = models.CharField(
        max_length=20, 
        choices=REFERRAL_STATUS_CHOICES, 
        default='pending'
    )
    referral_completed_at = models.DateTimeField(null=True, blank=True)
    referral_notes = models.TextField(blank=True)
    is_referred = models.BooleanField(default=False)
    referred_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['-created_at']