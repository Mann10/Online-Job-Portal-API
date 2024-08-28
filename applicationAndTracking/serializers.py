from rest_framework import serializers
from .models import ApplicationModel
from django.utils import timezone

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model=ApplicationModel
        exclude=('status','user')
        
    def validate(self, attrs):
        current_user_id=self.context['request'].user.id
        print(current_user_id)
        current_job_id=attrs['job'].id
        if not attrs['job'].is_active:
            raise serializers.ValidationError({"Alert":"This job posting is not opened."})
        if self.context['request'].user.is_employer:
            raise serializers.ValidationError({"Alert":"Employer's aren't alloweded to submit the application"})
        if ApplicationModel.objects.filter(user_id=current_user_id,job_id=current_job_id).exists():
            raise serializers.ValidationError({"Alert":"You have already applied for this job post!"})
            
        return super().validate(attrs)
    

    
class NotificationSerializer(serializers.Serializer):
    user=serializers.CharField() # This is the user to which notify model will send notification.
    message=serializers.CharField()
    notification_type=serializers.CharField(max_length=120)
    is_read=serializers.BooleanField(default=False)
    timestamp=serializers.DateTimeField()
    