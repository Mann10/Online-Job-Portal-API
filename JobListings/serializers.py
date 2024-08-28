from rest_framework import serializers
from .models import JobModel

class JobModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=JobModel
        fields='__all__'
        
    def validate(self, attrs):
        print(attrs)
        print(self.context['request'].user.is_employer)
        request = self.context.get('request')
        print(request)
        if not request.user.is_employer:
            raise serializers.ValidationError({"message":"Only employees could add job post."})
        if 'company' in attrs:
            print(attrs['company'])
            if not attrs.get('company').is_employer:
                raise serializers.ValidationError({'message':f'You are not alloweded to create a job posting. As your role is not employer.'})
        return super().validate(attrs)
        