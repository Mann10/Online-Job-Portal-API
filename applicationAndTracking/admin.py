from django.contrib import admin
from .models import ApplicationModel,NotificationModel

# Register your models here.
admin.site.register(ApplicationModel)
admin.site.register(NotificationModel)