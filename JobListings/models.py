from django.db import models
from users.models import CustomUserModel

# Create your models here.

class JobModel(models.Model):
    employment_type_choices=[('ft','Full-time'),('pt','part-time'),('c','contract')]
    title=models.CharField(max_length=150)
    description=models.TextField()
    location=models.CharField(max_length=100)
    salary_range=models.CharField(max_length=50,null=True,blank=True)
    employment_type=models.CharField(max_length=50,choices=employment_type_choices)
    company=models.ForeignKey(CustomUserModel,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField()
    
    def __str__(self) -> str:
        return self.title
