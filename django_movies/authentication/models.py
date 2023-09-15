from django.db import models
from django.contrib.auth.models import User


class CustomProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='custom_profile')
    profile_pic = models.ImageField(upload_to='profile_pics', null=True, blank=True)
