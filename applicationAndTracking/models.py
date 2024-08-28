from django.db import models
from users.models import CustomUserModel
from JobListings.models import JobModel
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone



# Create your models here.

class ApplicationModel(models.Model):
    application_status=[('submitted', 'Submitted'),('in_review', 'In Review'),('rejected', 'Rejected'),('accepted', 'Accepted')]
    user=models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    job=models.ForeignKey(JobModel, on_delete=models.CASCADE)
    status=models.CharField(max_length=50,choices=application_status)
    applied_date=models.DateTimeField(auto_now_add=True)
    cover_letter=models.TextField()
    resume=models.FileField(upload_to='Files', max_length=100)
    
    def __str__(self) -> str:
        return self.job.title

class NotificationModel(models.Model):
    user=models.ForeignKey(CustomUserModel, on_delete=models.CASCADE) # This is the user to which notify model will send notification.
    application_id=models.ForeignKey(ApplicationModel, on_delete=models.CASCADE)
    message=models.TextField()
    notification_type=models.CharField(max_length=120,choices=[('application_status_update','application_status_update'),('new_application','new_application')])
    is_read=models.BooleanField(default=False)
    timestamp=models.DateTimeField( auto_now_add=True)
    
    def __str__(self) -> str:
        return f"Notification for :- {self.user}"

@receiver(post_save,sender=ApplicationModel)
def notify_employer_newapplication(sender,instance,**kwargs):
    if instance.status=='submitted':
        notify_payload=NotificationModel()
        notify_payload.user=instance.job.company
        notify_payload.message=f"You got new application for your job {instance.job.title} and applicant name is {instance.user}"
        notify_payload.notification_type='new_application'
        notify_payload.is_read=False
        notify_payload.timestamp=timezone.now()
        notify_payload.application_id=instance
        notify_payload.save()
    elif instance.status=='accepted':
        notify_payload=NotificationModel()
        notify_payload.user=instance.user
        notify_payload.message=f"Congratulations your application has been accepted and you will receive a email for interview details soon!"
        notify_payload.notification_type='application_status_update'
        notify_payload.is_read=False
        notify_payload.timestamp=timezone.now()
        notify_payload.application_id=instance
        notify_payload.save()
    elif instance.status=='rejected':
        notify_payload=NotificationModel()
        notify_payload.user=instance.user
        notify_payload.message=f"Sorry your application is rejected. Please try again in the company after 6 months."
        notify_payload.notification_type='application_status_update'
        notify_payload.is_read=False
        notify_payload.timestamp=timezone.now()
        notify_payload.application_id=instance
        notify_payload.save()
    else:
        pass


@receiver(post_save,sender=NotificationModel)
def notify_applicant_when_readed(sender,instance,**kwargs):
    if instance.is_read:
        related_application = ApplicationModel.objects.get(id=instance.application_id.id)  # Use a proper lookup to find the application

        # Check current status and update to 'in_review'
        if related_application.status == 'submitted':
            related_application.status = 'in_review'
            related_application.save()

            # Create a new notification for the applicant
            NotificationModel.objects.create(
                user=related_application.user,
                message=f"Your application for {related_application.job.title} is now in review.",
                notification_type='application_status_update',
                application_id=related_application,
                timestamp=timezone.now(),
                is_read=False
            )

    
      
    
