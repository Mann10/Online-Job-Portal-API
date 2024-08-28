from rest_framework import serializers
from .models import CustomUserModel

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUserModel
        fields=['username','password','email','is_employer','company_name','company_description','resume','contact_info']
    
    def validate(self,data):
        
        if 'is_employer' not in data:
            raise serializers.ValidationError({"is_employer": "This field is required!"})
        
        if 'contact_info' not in data:
            raise serializers.ValidationError({"contact_info": "This field is required!"})
        
        if 'email' not in data:
            raise serializers.ValidationError({"email": "This field is required!"})
        if data['is_employer']:
            if 'company_name' not in data or not data['company_name'].strip() :
                raise serializers.ValidationError({'company_name':'company_name field is required!!'})
            elif 'company_description' not in data or not data['company_description'].strip() :
                raise serializers.ValidationError({'company_description':'company_name field is required!!'})
            elif 'resume' in data:
                raise serializers.ValidationError({'resume':'This field is only for job seekers!!'})
        else:
            
            if 'resume' not in data :
                raise serializers.ValidationError({'resume':'Please upload your resume.'})
            elif 'company_name' in data:
                raise serializers.ValidationError('You are not alloweded to enter company_name as you are job seeker.')
            elif 'company_description' in data:
                raise serializers.ValidationError('You are not alloweded to enter company_description as you are job seeker')
        return data
    
    def create(self,validated_data):
        return CustomUserModel.objects.create_user(**validated_data)
            
        

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
     
    def validate(self, attrs):
        print(attrs)
        if 'username' not in attrs:
            raise serializers.ValidationError({'username':'This field is required'})
        if 'password' not in attrs:
            raise serializers.ValidationError({'password':'This field is required'})
        return super().validate(attrs) 
               
               