from django.shortcuts import render,get_object_or_404
from .models import ApplicationModel,NotificationModel
from JobListings.models import JobModel
from .serializers import ApplicationSerializer,NotificationSerializer
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from .custom_permissions import IsEmployerAndUpdateApplication
from rest_framework import status



class ApplicationView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
    def post(self,request):
        ser=ApplicationSerializer(data=request.data,context={'request':request})
        if ser.is_valid():
            ser.validated_data['status']='submitted'
            ser.validated_data['user']=self.request.user
            ser.save()
            return Response(ser.data,status.HTTP_201_CREATED)
        return Response(ser.errors,status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class ApplicationViewEmployer(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
    def get(self,request,job_id):
        current_looged_employer_id=request.user.id
        print(current_looged_employer_id)
        if JobModel.objects.filter(company_id=current_looged_employer_id).exists():
            applications=ApplicationModel.objects.filter(job_id=job_id)
            ser=ApplicationSerializer(applications,many=True)
            return Response(ser.data,status.HTTP_200_OK)
        return Response({"message":"Sorry you cannot see job applicaions of the job postings that you haven't created"},status.HTTP_403_FORBIDDEN)

           
class ApplicationDetailViewEmployer(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self, request, id):
        current_logged_employer_id = request.user.id

        try:
            application = ApplicationModel.objects.get(id=id)
            if application.job.company.id != current_logged_employer_id:
                return Response(
                    {"message": "Sorry, you cannot view this application."},status.HTTP_403_FORBIDDEN)
            
        except ApplicationModel.DoesNotExist:
            return Response(
                {"message": "Application not found."},status.HTTP_404_NOT_FOUND)
            
        ser = ApplicationSerializer(application)
        return Response(ser.data,status=status.HTTP_200_OK)

class NotificationListView(APIView):
    def get(self,request):
        get_all_notification=NotificationModel.objects.all()
        ser=NotificationSerializer(get_all_notification,many=True)
        return Response(ser.data,status=status.HTTP_200_OK)
    
    
class NotificationReadView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated,IsEmployerAndUpdateApplication]
    def post(self,request,notify_id):
        notification=get_object_or_404(NotificationModel,id=notify_id) 
        #Here we are validating if the application belongs to logged in employer or not.
        application=get_object_or_404(ApplicationModel,id=notification.application_id.id)
        self.check_object_permissions(request,application)
        notification.is_read=True
        notification.save(update_fields=['is_read'])
        return Response("You have marked this notification as read.",status.HTTP_201_CREATED)
    
    def delete(self,request,id):
        obj=get_object_or_404(NotificationModel,id=id)
        obj.delete()
        return Response("Notification Deleted successfully",status.HTTP_200_OK)
        
class MarkApplicationAsRejectedOrAccepted(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated,IsEmployerAndUpdateApplication]
    
    def post(self,request,application_id):
        notification_updated=get_object_or_404(ApplicationModel,id=application_id)
        self.check_object_permissions(request,notification_updated)
        notification_updated.status=request.data.get('status')
        notification_updated.save(update_fields=['status'])
        return Response(f"You have marked this application as {notification_updated.status}",status.HTTP_201_CREATED)