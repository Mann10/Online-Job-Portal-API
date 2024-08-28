from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUserModel(AbstractUser):
    is_employer=models.BooleanField(default=False)
    company_name=models.CharField(max_length=150,null=True,blank=True)
    company_description=models.CharField(max_length=250,null=True,blank=True)
    resume=models.FileField(upload_to='Files', max_length=100,null=True,blank=True)
    contact_info=models.JSONField(null=True,blank=True)
    
