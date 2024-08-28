from django.urls import path
from .views import Registration,LoginView,ProfileUpdate

urlpatterns = [
    
    path('register/',Registration.as_view(),name='register/profile'),
    path('login/',LoginView.as_view(),name='login'),
    path('profile/<int:id>/',ProfileUpdate.as_view(),name='profile-id'),

]