from django.shortcuts import render
from .models import JobModel
from .serializers import JobModelSerializer
from .filters import JobFilters

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from .custom_permission import IsEmployerUpdateOwnJob

from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

class JobView(ModelViewSet):
    queryset=JobModel.objects.all()
    serializer_class=JobModelSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated,IsEmployerUpdateOwnJob]


    def get_queryset(self):
        if self.request.method=='GET':
            queryset=JobModel.objects.filter(is_active=True)
            return queryset
        return super().get_queryset()
    
    def get_object(self):
        if self.request.method=='PUT':
            self.check_object_permissions(self.request,super().get_object())
        return super().get_object()
    
    def destroy(self, request, *args, **kwargs):
        instance=self.get_object()
        instance.delete()
        return Response({'alert':'Item deleted successfully!'})
        
class JobSearch(ListAPIView):
    queryset=JobModel.objects.filter(is_active=True)
    serializer_class=JobModelSerializer
    filter_backends=[DjangoFilterBackend]
    filterset_class=JobFilters
    
