from django.urls import path
from .views import ApplicationView,ApplicationViewEmployer,ApplicationDetailViewEmployer,NotificationListView,NotificationReadView,MarkApplicationAsRejectedOrAccepted

urlpatterns = [
    path('applications/',ApplicationView.as_view(),name='application-create'),
    #api/applications/?job_id=<job_id>
    path('applications/<int:job_id>/',ApplicationViewEmployer.as_view(),name='application-view'),
    path('application/<int:id>/',ApplicationDetailViewEmployer.as_view(),name='application-deatil-view'),
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:notify_id>/read/', NotificationReadView.as_view(), name='notification-read'),
    path('notifications/<int:id>/delete/', NotificationReadView.as_view(), name='notification-read'),
    path('markas/<int:application_id>/', MarkApplicationAsRejectedOrAccepted.as_view(), name='MarkasRejectedoraccepted'),
]