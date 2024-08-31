from rest_framework import serializers
from .models import JobModel

class JobModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=JobModel
        exclude=('company',)
        #fields='__all__'
        
    def validate(self, attrs):  
        request = self.context.get('request')
        if not request:
            raise serializers.ValidationError({"message": "Request context is missing."})

    # Check if the user is authenticated
        if not request.user.is_authenticated:
            raise serializers.ValidationError({"message": "Authentication credentials were not provided."})
    
        if not request.user.is_employer:
            raise serializers.ValidationError({"message":"Only employees could add job post."})
        
        if 'company' in attrs:  
            if not attrs['company'].is_employer:
                raise serializers.ValidationError({'message':f'You are not alloweded to create a job posting. As your role is not employer.'})
        return attrs

    def create(self, validated_data):
        validated_data['company'] = self.context['request'].user
        return super().create(validated_data)
    
    
         