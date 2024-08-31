from django.shortcuts import render
from .models import JobModel
from .serializers import JobModelSerializer
from .filters import JobFilters

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from .custom_permission import IsEmployerUpdateOwnJob
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

class JobView(ModelViewSet):
    queryset=JobModel.objects.all()
    serializer_class=JobModelSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated,IsEmployerUpdateOwnJob]


    def get_queryset(self):
        if self.action == 'list' or self.action == 'retrieve':
            return JobModel.objects.filter(is_active=True,company=self.request.user)
        return super().get_queryset()
    

    def destroy(self, request, *args, **kwargs):
        instance=self.get_object()
        instance.delete()
        return Response({'alert':'Item deleted successfully!'})
    
    
    def update(self, request, *args, **kwargs):
        instance=self.get_object()
        self.check_object_permissions(request,instance)
        ser=self.get_serializer(instance,data=request.data,partial=kwargs.get('partial', False))
        if ser.is_valid():
            ser.validated_data['company']=request.user
            self.perform_update(ser)
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
 
        
class JobSearch(ListAPIView):
    queryset= JobModel.objects.all()
    serializer_class=JobModelSerializer
    filter_backends=[DjangoFilterBackend]
    filterset_class=JobFilters
    
