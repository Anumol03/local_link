from django.db import models
from django.contrib.auth.models import AbstractUser

class Ward(models.Model):
    ward_no=models.PositiveIntegerField()
    house_no=models.PositiveIntegerField()
    name=models.CharField(max_length=200)

    def __str__(self) :
        return self.name
    
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('service', 'Service'),
        ('citizen', 'Citizen'),
    ]

    email = models.EmailField(unique=True)
    ward_no = models.CharField(max_length=10)
    house_no = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    adhar_no = models.CharField(max_length=12, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.username