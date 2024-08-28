from django.shortcuts import render,get_list_or_404
from .serializers import RegistrationSerializer,LoginSerializer
from django.contrib.auth import authenticate
from .models import CustomUserModel

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

class Registration(APIView):
    
    def get(self,request):
        users_profiles=CustomUserModel.objects.all()
        ser=RegistrationSerializer(users_profiles,many=True)
        for item in ser.data:
            if 'password' in item:
                item.pop('password')
        return Response(ser.data,status=status.HTTP_200_OK)
                
        
    
    def post(self,request):
        ser=RegistrationSerializer(data=request.data)
        #breakpoint()--USED TO STOP THE CURSOR WHILE RUNNING THE APPLICATION USE (Pdb) ser to see what's in serializer.
        if ser.is_valid():
            ser.save()
            return Response(ser.data,status=status.HTTP_201_CREATED)
        return Response(ser.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    
    def post(self,request):
        ser=LoginSerializer(data=request.data)
        if ser.is_valid():
            username=ser.validated_data.get('username')
            password=ser.validated_data.get('password')
            
            user=authenticate(username=username,password=password)
            if user:
                refresh = RefreshToken.for_user(user)

                return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                                })
            return Response("Invalid username or password. Try again!",status=status.HTTP_401_UNAUTHORIZED)
        return Response(ser.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class ProfileUpdate(APIView):
    def get(self,request,id):
        try:
            user_details=CustomUserModel.objects.get(id=id)
        except CustomUserModel.DoesNotExist:
            return Response("User dosen't exists!")
        ser=RegistrationSerializer(user_details)
        data=ser.data.copy()
        if 'password' in data:
            data.pop('password')
        return Response(data,status=status.HTTP_200_OK)
    
    def put(self,request,id):
        user_profile=CustomUserModel.objects.get(id=id)
        ser=RegistrationSerializer(instance=user_profile,data=request.data,partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data,status=status.HTTP_200_OK)
        return Response(ser.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)